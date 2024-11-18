<template>
  <div>
    <Navbar></Navbar>
    <div class="container">
      <h1 style="text-align: center">Librarian's Dashboard</h1>
      <p>
        Welcome to your dashboard. This is exclusively visible only to the
        admin, the librarian. Browse through the books in your library, the
        sections, and the members of this library, all at one place. This page
        is not meant to be exhaustive, but to be helpful.
      </p>
      <p>
        Click on the books icon to view the books page in more detail. Same goes
        for the sections, and users. You can view your own profile by clicking
        here, or on the profile icon up on the navigation bar.
      </p>
      <div style="text-align: center">
        <router-link class="btn btn" to="/display/books"
          >View Books</router-link
        >
        <router-link class="btn btn" to="/display/sections"
          >View Sections</router-link
        >
        <router-link class="btn btn" to="/display/users"
          >View Users</router-link
        >
        <router-link class="btn btn" :to="'/profile/' + user_id"
          >Your Profile</router-link
        >
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from "@/components/Navbar.vue";
export default {
  data() {
    return {
      user_id: "",
    };
  },
  components: {
    Navbar,
  },
  async created() {
    this.user_id = localStorage.getItem("user_id");
  },
};
</script>

<style>
</style>