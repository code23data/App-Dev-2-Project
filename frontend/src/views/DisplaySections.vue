<template>
  <div>
    <Navbar></Navbar>
    <div class="container">
      <h1>View Sections</h1>
      <form class="form-inline my-2" @submit.prevent="searchSection">
        <input
          class="form-control mr-sm-2"
          type="search"
          placeholder="Search"
          aria-label="Search"
          v-model="search_text"
        />
      </form>
      <ul
        class="list-group"
        v-for="section in filteredSections"
        :key="section.section_id"
      >
        <li class="list-group-item">
          <div>{{ section.section_name }}</div>
          <div class="ml-auto">
            <router-link
              v-if="isAdmin"
              class="btn btn-warning ml-2"
              :to="'/update/sections/' + section.section_id"
              >Update</router-link
            >
            <button
              v-if="isAdmin"
              class="btn btn-danger ml-2"
              @click="deleteSection(section.section_id)"
            >
              Delete
            </button>
            <router-link
              :to="'/display/section-books/' + section.section_id"
              class="btn btn-primary"
            >
              View Books
            </router-link>
          </div>
        </li>
      </ul>
    </div>
    <div v-if="isAdmin" class="text-center my-3">
      <router-link to="/add/sections" class="btn btn-secondary"
        >Add Section</router-link
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
      sections: [],
      isAdmin: false,
      search_text: "",
    };
  },
  components: {
    Navbar,
  },
  methods: {
    async deleteSection(section_id) {
      const token = localStorage.getItem("token");
      if (token) {
        try {
          const response = await axios.delete(`api/sections/${section_id}`, {
            headers: { Authorization: `Bearer ${token}` },
          });
          console.log(response);
          console.log("Section deleted successfully");
          this.sections = this.sections.filter(
            (section) => section.section_id != section_id
          );
        } catch {
          console.log("Error: Failed to delete the section");
        }
      }
    },
    async fetchAllSections() {
      try {
        const response = await axios.get("api/sections/all");
        this.sections = response.data;
        console.log("Successfully fetched the data");
      } catch (error) {
        console.error(error);
        console.log("Your request was not successful");
      }
    },
    async searchSection() {
      try {
        const response = await axios.get(
          `/sections/search=${this.search_text}`
        );
        this.sections = response.data;
        console.log("successful");
      } catch {
        console.log("Error: Failed to search");
      }
    },
  },
  async created() {
    await this.fetchAllSections();
    const token = localStorage.getItem("token");
    const isadmin = localStorage.getItem("isadmin");
    if (token) {
      if (isadmin === "true") {
        this.isAdmin = true;
      }
    }
  },
  computed: {
    filteredSections() {
      if (this.search_text) {
        return this.sections.filter((section) =>
          section.section_name
            .toLowerCase()
            .includes(this.search_text.toLowerCase())
        );
      } else {
        return this.sections;
      }
    },
  },
};
</script>
