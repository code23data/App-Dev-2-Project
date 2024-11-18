<template>
  <div>
    <Navbar></Navbar>
    <div class="container p-3 my-3">
      <h1>Sign In</h1>
      <div class="col-md-6">
        <form @submit.prevent="login">
          <div class="form-group">
            <label for="exampleInputEmail1">Username</label>
            <input
              type="text"
              class="form-control"
              id="exampleInputEmail1"
              aria-describedby="emailHelp"
              placeholder="Enter username"
              v-model="username"
              required
            />
            <small id="emailHelp" class="form-text text-muted"
              >We'll never share your username with anyone else.</small
            >
          </div>
          <div class="form-group">
            <label for="exampleInputPassword1">Password</label>
            <input
              type="password"
              class="form-control"
              id="exampleInputPassword1"
              placeholder="Password"
              v-model="password"
              required
            />
          </div>
          <br />
          <button type="submit" class="btn btn-primary">Submit</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from "@/components/Navbar.vue";
import axios from "axios";

axios.defaults.baseURL = "http://127.0.0.1:8080/";

export default {
  data() {
    return {
      username: "",
      password: "",
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post("/login", {
          username: this.username,
          password: this.password,
        });
        console.log(response);
        console.log("success");
        localStorage.setItem("token", response.data.access_token);
        localStorage.setItem("isadmin", response.data.is_admin);
        localStorage.setItem("user_id", response.data.user_id);
        this.$router.push("/");
      } catch (err) {
        console.log(err);
        console.log("Request failed");
      }
    },
  },
  components: {
    Navbar,
  },
};
</script>