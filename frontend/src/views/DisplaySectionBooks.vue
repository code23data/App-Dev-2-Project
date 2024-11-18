<template>
  <div>
    <Navbar></Navbar>
    <div class="container">
      <h1>View Books belonging to Section {{ section.section_name }}</h1>
      <form class="form-inline my-2" @submit.prevent="searchBook">
        <input
          class="form-control mr-sm-2"
          type="search"
          placeholder="Search"
          aria-label="Search"
          v-model="search_text"
        />
      </form>
      <ul class="list-group" v-for="book in filteredBooks" :key="book.book_id">
        <li class="list-group-item">
          <div>{{ book.book_name }} by {{ book.authors }}</div>
          <div class="ml-auto">
            <router-link
              class="btn btn-warning ml-2"
              :to="'/update/books/' + book.book_id"
              v-if="isAdmin"
              >Update</router-link
            >
            <button
              class="btn btn-danger ml-2"
              @click="deleteBook(book.book_id)"
              v-if="isAdmin"
            >
              Delete
            </button>
            <router-link
              :to="'/read/books/' + book.book_id"
              class="btn btn-primary ml-2"
              v-if="isAdmin || isIssued"
            >
              View Book
            </router-link>
            <button
              class="btn btn-info"
              @click="issueBook(book.book_id)"
              v-if="!isIssued && !isAdmin"
            >
              Issue Book
            </button>
            <button
              class="btn btn-info"
              @click="returnBook(book.book_id)"
              v-if="!isAdmin"
            >
              Return Book
            </button>
            <router-link
              class="btn btn-light"
              :to="'/display-reviews/' + book.book_id"
            >
              View Reviews
            </router-link>
            <button
              class="btn btn-dark"
              @click="canReview(book.book_id)"
              v-if="!isAdmin"
            >
              Write a Review
            </button>
          </div>
        </li>
      </ul>
    </div>
    <div v-if="isAdmin" class="text-center my-3">
      <router-link to="/add/books" class="btn btn-secondary"
        >Add Books</router-link
      >
    </div>
    <div class="text-center my-3">
      <router-link to="/display/sections" class="btn btn">
        Go Back
      </router-link>
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
      books: [],
      isAdmin: false,
      search_text: "",
      section: "",
      isIssued: false,
    };
  },
  components: {
    Navbar,
  },
  methods: {
    async issueBook(book_id) {
      const token = localStorage.getItem("token");
      try {
        const issued = await axios.post(
          `/issue_book/${book_id}`,
          {},
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        console.log(issued.data);
        alert("Book issued successfully");
      } catch (error) {
        if (error.response && error.response.data.error) {
          alert(error.response.data.error);
        } else {
          alert("An error occured");
          console.log(error);
        }
      }
    },
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
      } catch (error) {
        if (error.response && error.response.data.error) {
          alert(error.response.data.error);
        } else {
          alert("An error occured");
          console.log(error);
        }
      }
    },
    async canIssue(book_id) {
      const token = localStorage.getItem("token");
      const response = await axios.get(`api/books/${book_id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (response.data.user_id) {
        return false;
      } else {
        return true;
      }
    },
    async canReview(book_id) {
      const userID = localStorage.getItem("user_id");
      const token = localStorage.getItem("token");
      const response = await axios.get(`api/books/${book_id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const book = response.data;
      if (book.user_id == Number(userID)) {
        if (
          (book.date_issued && !book.date_returned) ||
          book.date_returned > book.date_issued
        )
          this.$router.push("/add-review/" + book.book_id);
        else alert("You have to issue a book before you can write a review");
      } else alert("You cannot write a review.");
    },
    async deleteBook(book_id) {
      const token = localStorage.getItem("token");
      if (token) {
        try {
          const response = await axios.delete(`api/books/${book_id}`, {
            headers: { Authorization: `Bearer ${token}` },
          });
          console.log(response);
          console.log("Book Deleted successfully");
          this.$router.go();
          this.books = this.books.filter((book) => book.book_id !== book_id);
        } catch {
          console.log("error");
          console.log("Failed to delete book");
        }
      }
    },
    async fetchAllBooks() {
      try {
        const response = await axios.get("api/books/all");
        this.books = response.data;
      } catch (error) {
        console.error(error);
      }
    },
    async searchBook() {
      try {
        const response = await axios.get(`/books/search=${this.search_text}`);
        this.books = response.data;
        console.log("successful");
      } catch {
        console.log("Error: Failed to search");
      }
    },
  },
  async created() {
    await this.fetchAllBooks();
    try {
      const token = localStorage.getItem("token");
      if (token) {
        const id = this.$route.params.id;
        const response = await axios.get(`api/sections/${id}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.section = response.data;
        console.log(response.data);
        this.books = this.section.books;
        if (localStorage.getItem("isadmin") === "true") {
          this.isAdmin = true;
          console.log(this.isAdmin);
        }
      }
    } catch (error) {
      console.error(error);
      console.log("Your request was not successful");
    }
  },
  computed: {
    filteredBooks() {
      if (this.search_text) {
        return this.section.books.filter((book) =>
          book.book_name.toLowerCase().includes(this.search_text.toLowerCase())
        );
      } else {
        return this.section.books;
      }
    },
  },
};
</script>
  
  
 