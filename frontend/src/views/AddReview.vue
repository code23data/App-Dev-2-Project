<template>
  <div class="container">
    <Navbar2></Navbar2>
    <h1>Write a review for the book</h1>
    <form @submit.prevent="addReview">
      <div class="form-group">
        <label for="name">Rating</label><br />
        <div v-for="i in 5" :key="i">
          <input
            type="radio"
            class="form-check-input"
            :name="'rating-option'"
            :id="`formGroupExampleInput-${i}`"
            :value="i"
            v-model="rating"
          />
          <label :for="`formGroupExampleInput-${i}`" class="form-check-label">
            {{ i }} </label
          ><br />
        </div>
      </div>

      <div class="form-group">
        <label for="post">Review Post</label>
        <textarea
          class="form-control"
          id="contentTextArea"
          rows="6"
          v-model="post"
        ></textarea>
      </div>
      <button type="submit" class="btn btn-primary">Submit</button>
      <router-link to="/display/books" class="btn btn">Cancel</router-link>
    </form>
  </div>
</template>

<script>
import Navbar2 from "@/components/Navbar2.vue";
import axios from "axios";

axios.defaults.baseURL = "http://127.0.0.1:8080/";
export default {
  data() {
    return {
      rating: 0,
      post: "",
      book: {},
    };
  },
  components: {
    Navbar2,
  },
  methods: {
    async addReview() {
      const token = localStorage.getItem("token");
      const id = this.$route.params.id;
      if (token) {
        try {
          if (this.book.date_issued && !this.book.date_returned) {
            const response = await axios.post(
              "api/reviews",
              {
                book_id: id,
                post: this.post,
                rating: this.rating,
              },
              {
                headers: { Authorization: `Bearer ${token}` },
              }
            );
            console.log(response);
            this.$router.push("/display/books");
          } else {
            alert("You cannot write a review if you haven't issued the book");
          }
        } catch (error) {
          console.log(error);
        }
      }
    },
  },
  async created() {
    const id = this.$route.params.id;
    const token = localStorage.getItem("token");

    try {
      const response_old = await axios.get(`api/books/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      this.book = response_old.data;
      console.log(this.book);
    } catch {
      console.log("Error: Could not fetch the book.");
    }
  },
};
</script>