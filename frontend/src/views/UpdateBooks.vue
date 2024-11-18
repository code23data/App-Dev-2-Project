<template>
  <div class="container">
    <Navbar2></Navbar2>
    <h1>Update Book</h1>
    <form @submit.prevent="updateBook">
      <div class="form-group">
        <label for="name">Book Name</label>
        <input
          type="text"
          class="form-control"
          id="formGroupExampleInput"
          :placeholder="old_book.book_name"
          v-model="book_name"
        />
      </div>
      <div class="form-group">
        <label for="authors">Authors (separate names by comma (,))</label>
        <input
          type="text"
          class="form-control"
          id="formGroupExampleInput2"
          :placeholder="old_book.authors"
          v-model="authors"
        />
      </div>
      <div class="form-group">
        <label for="section">Sections</label>
        <input
          type="text"
          class="form-control"
          id="formGroupExampleInput2"
          placeholder="first section, second section, ..."
          v-model="sections"
        />
        <ul v-for="section in sections_display" :key="section.section_id">
          <li>{{ section.section_name }}</li>
        </ul>
      </div>
      <div class="form-group">
        <label for="content">Book Content</label>
        <textarea
          class="form-control"
          id="contentTextArea"
          rows="6"
          :placeholder="old_book.content"
          v-model="content"
        ></textarea>
      </div>
      <button type="button" @click="updateBook" class="btn btn-primary">
        Submit
      </button>
      <router-link to="/display/books" class="btn btn">Go Back</router-link>
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
      sections_display: [],
      book_name: "",
      authors: "",
      sections: "",
      content: "",
      old_book: {},
    };
  },
  components: {
    Navbar2,
  },
  methods: {
    isName(str) {
      return str.length > 0;
    },
    isAuthor(str) {
      return str.length > 0;
    },
    isContent(str) {
      return str.length > 0;
    },
    async updateBook() {
      const id = this.$route.params.id;
      const token = localStorage.getItem("token");
      const isadmin = localStorage.getItem("isadmin");
      const re = /\s*(?:,|$)\s*/;
      if (token) {
        if (isadmin === "true") {
          try {
            const newBook = await axios.put(
              `api/books/${id}`,
              {
                book_name: this.book_name,
                authors: this.authors,
                sections: this.sections.trim().split(re),
                content: this.content,
              },
              {
                headers: { Authorization: `Bearer ${token}` },
              }
            );
            console.log(newBook);
            console.log("successful");

            alert("Book Updated Successfully");

            this.$router.push("/display/books");
          } catch (error) {
            console.log(error);
            console.log("Request failed");
          }
        }
      } else {
        console.log(
          "Not logged in, so cannot add new book. Please login with admin ID."
        );
      }
    },
  },
  async created() {
    try {
      const response = await axios.get("/api/sections/all");
      console.log(response.data);
      this.sections_display = response.data;
    } catch (error) {
      console.log(error);
      console.log("Failed to fetch section names correctly");
    }
    const id = this.$route.params.id;
    const token = localStorage.getItem("token");
    try {
      const response_old = await axios.get(`api/books/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      this.old_book = response_old.data;
      console.log(this.old_book);
    } catch {
      console.log("Error: Could not fetch the book.");
    }
  },
};
</script>