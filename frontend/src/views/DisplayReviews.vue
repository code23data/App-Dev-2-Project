<template>
  <div class="container">
    <Navbar></Navbar>
    <h1>Reviews for {{ book_name }}</h1>
    <br />
    <ul class="list-group" v-for="review in reviews" :key="review.roll">
      <li class="list-group-item">
        <h3>{{ review.rating }}/5</h3>
        <div>{{ review.post }}</div>
      </li>
    </ul>
    <div class="text-center my-3">
      <router-link to="/display/books" class="btn btn-secondary"
        >Go Back</router-link
      >
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Navbar from "@/components/Navbar.vue";

axios.defaults.baseURL = "http://127.0.0.1:8080/";
export default {
  data() {
    return {
      reviews: [],
      book_name: "",
    };
  },
  components: {
    Navbar,
  },
  async created() {
    const id = this.$route.params.id; //book ID
    const token = localStorage.getItem("token");
    const response = await axios.get(`api/books/${id}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    this.reviews = response.data.reviews;
    console.log(this.reviews);
    this.book_name = response.data.book_name;
  },
};
</script>

<style>
</style>