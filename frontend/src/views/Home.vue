<template>
  <div>
    <Navbar></Navbar>

    <div class="container my-3" v-if="!isLoggedIn">
      <h1 style="text-align: center">Library Management System</h1>
      <p>
        Welcome to Library Management System (LMS). Here, you can explore a wide
        range of books, consisting of different sections and genres. Whether you
        like fiction or non-fiction, education or entertainment, science or
        finance, there is always something to cater to your reading needs! So
        feel free to explore the library, and have the opportunity to issue
        books digitally! We promise that there is something that will catch your
        eye, and hope to see you there!
      </p>
      <h2 style="text-align: center">Get Started Now!</h2>
      <p>
        Now that you know who we are, and what we have to offer, why not
        <router-link to="/register/user">sign-up</router-link>, and explore the
        books we have to offer? There is so much convenience we have: all you
        need is to click on a book that is available, issue it, and read it as
        you wish. We also provide a download option for those who want to keep a
        copy to themselves! So what are you waiting for? Click on the Register
        button on the top right now!
      </p>
    </div>
    <div class="container" v-else-if="isLoggedIn && !isAdmin">
      <h1 style="text-align: center">Welcome!</h1>
      <p>
        We request you to return back the books once you have finished reading.
        They will automatically be revoked from access for you after a week, so
        beware of that!
      </p>
      <p>
        Please browse through our catalog of interesting
        <router-link to="/display/books">books</router-link>, and see if there
        is anything that catches your eye! Happy exploring!
      </p>
    </div>
    <div class="container" v-else>
      <h1 style="text-align: center">Welcome!</h1>
      <p>
        Welcome back, Librarian! We are pleased to have you back here. Please
        feel free to do as you please! Have a look at your
        <router-link to="/dashboard">dashboard</router-link> to know more about
        the users and the sections, and get to know more about them!
      </p>
      <p>
        While being a librarian, you are also a reader. So, please browse
        through our catalog of interesting books, and see if there is anything
        that catches your eye! Happy exploring!
      </p>
    </div>
  </div>
</template>

<script>
import Navbar from "../components/Navbar.vue";
import axios from "axios";

axios.defaults.baseURL = "http://127.0.0.1:8080/";

export default {
  name: "Home",
  components: {
    Navbar,
  },
  data() {
    return {
      isLoggedIn: false,
      isAdmin: false,
    };
  },
  async created() {
    const token = localStorage.getItem("token");
    const isadmin = localStorage.getItem("isadmin");
    if (token) {
      this.isLoggedIn = true;
    }
    if (isadmin == "true") {
      this.isAdmin = true;
    }
  },
};
</script>
    