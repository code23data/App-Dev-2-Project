<template>
  <div>
    <Navbar></Navbar>
    <div class="container" v-if="user">
      <h1>Hello! How are you, {{ user.username }}?</h1>
      <h2>Here is your profile:</h2>
      <h3>Personal Details</h3>
      <ul>
        <li>Username : {{ user.username }}</li>
        <li>E-mail: {{ user.email }}</li>
        <li>Your Unique User ID: {{ user.user_id }}</li>
      </ul>

      <div v-if="!isAdmin">
        <h3>Books Issued</h3>
        <p v-if="issued_books.length == 0">You have not issued any books</p>
        <p v-else>You have issued {{ issued_books.length }} books. Namely,</p>
        <ul class="list-group" v-for="book in issued_books" :key="book.user_id">
          <li class="list-group-item">
            <div class="ml-auto">{{ book["book_name"] }}</div>
            <div>
              <router-link
                :to="'/read/books/' + book.book_id"
                class="btn btn-primary ml-2"
              >
                View Book
              </router-link>
              <button class="btn btn-info" @click="returnBook(book.book_id)">
                Return Book
              </button>
            </div>
          </li>
        </ul>
      </div>
    </div>
    <div v-else>Loading...</div>
  </div>
</template>

<script>
import Navbar from "@/components/Navbar.vue";
import axios from "axios";

axios.defaults.baseURL = "http://127.0.0.1:8080/";
export default {
  name: "ProfileView",
  components: {
    Navbar,
  },
  data() {
    return {
      isLoggedIn: false,
      user: {},
      isAdmin: false,
      issued_books: [],
    };
  },
  methods: {
    async returnBook(book_id) {
      const token = localStorage.getItem("token");
      try {
        const response = await axios.post(
          `/return_book/${book_id}`,
          {},
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        console.log(response.data);
        alert("Book returned successfully");
        this.$router.go();
      } catch (error) {
        if (error.response && error.response.data.error) {
          alert(error.response.data.error);
        } else {
          alert("An error occured");
          console.log(error);
        }
      }
    },
  },
  async created() {
    const token = localStorage.getItem("token");
    const isadmin = localStorage.getItem("isadmin");
    if (token) {
      this.isLoggedIn = true;
    }
    if (isadmin === "true") {
      this.isAdmin = true;
    }
    const userid = this.$route.params.userid;
    console.log(userid);
    const response = await axios.get(`api/users/${userid}`, {
      headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
    });
    console.log(response.data);
    this.user = response.data;
    this.issued_books = response.data.issued_books;
  },
};
</script>