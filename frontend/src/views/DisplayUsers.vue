<template>
  <div class="container">
    <Navbar></Navbar>
    <h1>List of Users</h1>
    <br />
    <ul class="list-group" v-for="user in users" :key="user.user_id">
      <li class="list-group-item">
        <div>Username : {{ user.username }}</div>
        <div>E-mail : {{ user.email }}</div>
        <div>User ID : {{ user.user_id }}</div>
        <div v-if="user.issued_books.length > 0">
          Issued Books :
          <ul v-for="book in user.issued_books" :key="book.book_id">
            <li>{{ book.book_name }}</li>
          </ul>
        </div>
        <div v-else>Has not issued any books</div>
        <div>Last Seen: {{ new Date(user.lastseen) }}</div>
        <div>
          <button
            class="btn btn-danger"
            @click="revokeAccess(user.user_id)"
            v-if="
              Boolean(user.is_admin) == false && user.username != '[deleted]'
            "
          >
            Revoke Access to Library
          </button>
        </div>
      </li>
    </ul>
    <div class="text-center my-3">
      <router-link to="/dashboard" class="btn btn-secondary"
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
      users: [],
    };
  },
  components: {
    Navbar,
  },
  methods: {
    async revokeAccess(userID) {
      const token = localStorage.getItem("token");
      const isadmin = localStorage.getItem("isadmin");
      if (token) {
        if (isadmin === "true") {
          const response = await axios.put(
            `api/users/${userID}`,
            { username: "[deleted]" },
            {
              headers: { Authorization: `Bearer ${token}` },
            }
          );
          console.log(userID);
          console.log(response);
        }
      }
    },
  },
  async created() {
    const token = localStorage.getItem("token");
    if (token) {
      try {
        const response = await axios.get("api/users/all", {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.users = response.data;
        console.log(response);
      } catch (error) {
        console.log(error);
        console.log("Error in fetching data");
      }
    }
  },
};
</script>