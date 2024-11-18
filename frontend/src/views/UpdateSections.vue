<template>
  <div class="container">
    <Navbar2></Navbar2>
    <h1>Update Section: {{ old_section.section_name }}</h1>
    <form @submit.prevent="updateSection">
      <div class="form-group">
        <label for="name">New Section Name</label>
        <input
          type="text"
          class="form-control"
          id="formGroupExampleInput"
          :placeholder="old_section.section_name"
          v-model="name"
        />
      </div>
      <div class="form-group">
        <label for="note"
          >An updated brief description of what the section is about</label
        >
        <textarea
          class="form-control"
          id="contentTextArea"
          rows="6"
          :placeholder="old_section.description"
          v-model="description"
        ></textarea>
      </div>
      <button type="button" @click="updateSection" class="btn btn-primary">
        Submit
      </button>
      <router-link to="/display/sections" class="btn btn">Cancel</router-link>
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
      name: "",
      description: "",
      old_section: [],
    };
  },
  components: {
    Navbar2,
  },
  methods: {
    isName(str) {
      return str.length > 0;
    },
    isDescription(str) {
      return str.length > 0;
    },
    async updateSection() {
      const token = localStorage.getItem("token");
      const isadmin = localStorage.getItem("isadmin");
      const id = this.$route.params.id;
      if (token) {
        if (isadmin === "true") {
          const response = await axios.put(
            `api/sections/${id}`,
            {
              name: this.name,
              description: this.description,
            },
            {
              headers: { Authorization: `Bearer ${token}` },
            }
          );
          console.log(response);
          console.log("Successfully updated section");
          this.$router.push("/display/sections");
        }
      }
    },
  },
  async created() {
    const id = this.$route.params.id;
    const token = localStorage.getItem("token");
    const response_get = await axios.get(`/api/sections/${id}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    this.old_section = response_get.data;
    console.log(this.old_section);
  },
};
</script>