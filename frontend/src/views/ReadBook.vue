<template>
  <div class="container">
    <Navbar></Navbar>
    <div id="export-to-pdf">
      <h1 style="text-align: center">{{ book_name }}</h1>
      <h2 style="text-align: center">by {{ authors }}</h2>
      <p>
        {{ content }}
      </p>
    </div>
    <div class="text-center my-3">
      <router-link to="/display/books" class="btn btn-secondary">
        Go Back
      </router-link>
    </div>
    <div class="text-center my-3">
      <button @click="exportToPDF" class="btn btn-primary">Buy the Book</button>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import html2pdf from "html2pdf.js";
import Navbar from "@/components/Navbar.vue";

axios.defaults.baseURL = "http://127.0.0.1:8080/";
export default {
  data() {
    return {
      book_name: "",
      authors: "",
      content: "",
    };
  },
  components: {
    Navbar,
  },
  methods: {
    exportToPDF() {
      html2pdf(document.getElementById("export-to-pdf"), {
        margin: 1,
        filename: `${this.book_name}.pdf`,
      });
    },
  },
  async created() {
    const id = this.$route.params.id;
    const token = localStorage.getItem("token");
    try {
      const response = await axios.get(`api/books/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      this.book_name = response.data.book_name;
      this.authors = response.data.authors;
      this.content = response.data.content;
    } catch (error) {
      console.log(error);
      console.log("Failed to get the data");
    }
  },
};
</script>

<style>
</style>