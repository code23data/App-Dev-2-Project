<template>
  <div>
    <nav class="navbar navbar-expand-md">
      <div class="container-fluid">
        <router-link class="navbar-brand" to="/">
          <img
            src="../assets/book.png"
            alt="Logo"
            width="30"
            height="24"
            class="d-inline-block align-text-top"
          />
          Library Management System
        </router-link>
        <ul class="navbar-nav d-flex">
          <li class="nav-item">
            <router-link to="/" class="nav-link">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/about">About</router-link>
          </li>
          <li class="nav-item" v-if="!isLoggedIn">
            <router-link class="nav-link" to="/login">Sign In</router-link>
          </li>
          <li class="nav-item" v-if="!isLoggedIn">
            <router-link class="nav-link" to="/register/user"
              >Register as User</router-link
            >
          </li>
          <li class="nav-item" v-if="isLoggedIn">
            <router-link class="nav-link" to="/display/books"
              >Books</router-link
            >
          </li>
          <li class="nav-item" v-if="isLoggedIn">
            <router-link class="nav-link" to="/display/sections"
              >Sections</router-link
            >
          </li>
          <li class="nav-item" v-if="isAdmin">
            <router-link class="nav-link" to="/dashboard"
              >Dashboard</router-link
            >
          </li>
          <li class="nav-item" v-if="isLoggedIn">
            <router-link class="nav-link" :to="'/profile/' + user_id"
              >Profile</router-link
            >
          </li>
          <li class="nav-item" v-if="isLoggedIn">
            <a class="nav-link" @click="logout">Logout</a>
          </li>
        </ul>
      </div>
    </nav>
  </div>
</template>

<script>
export default {
  name: "Navbar",
  data() {
    return {
      isLoggedIn: false,
      isAdmin: false,
      user_id: "",
    };
  },
  async created() {
    const token = localStorage.getItem("token");
    if (token) {
      this.isLoggedIn = true;
    }
    if (localStorage.getItem("user_id")) {
      this.user_id = localStorage.getItem("user_id");
    }
    if (localStorage.getItem("isadmin") === "true") {
      this.isAdmin = true;
    }
  },
  methods: {
    logout() {
      localStorage.removeItem("token");
      localStorage.removeItem("isadmin");
      localStorage.removeItem("user_id");
      this.$router.push("/login");
    },
  },
};
</script>