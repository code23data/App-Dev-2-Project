<template>
  <div class="container">
    <Navbar2></Navbar2>
    <form @submit.prevent="addSection">
      <div class="form-group">
        <label for="name">Section Name</label>
        <input
          type="text"
          class="form-control"
          id="formGroupExampleInput"
          placeholder="Section name"
          v-model="name"
        />
      </div>
      <div class="form-group">
        <label for="note"
          >A brief description of what the section is about</label
        >
        <textarea
          class="form-control"
          id="contentTextArea"
          rows="6"
          v-model="description"
        ></textarea>
      </div>
      <button type="button" @click="addSection" class="btn btn-primary">
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
    async addSection() {
      const token = localStorage.getItem("token");
      const isadmin = localStorage.getItem("isadmin");
      if (token) {
        if (isadmin === "true") {
          if (this.isName(this.name) && this.isDescription(this.description)) {
            const response = await axios.post(
              "api/sections",
              {
                name: this.name,
                description: this.description,
              },
              {
                headers: { Authorization: `Bearer ${token}` },
              }
            );
            console.log(response);
            console.log("Successfully added section");
            this.$router.push("/display/sections");
          }
        }
      }
    },
  },
};
</script>