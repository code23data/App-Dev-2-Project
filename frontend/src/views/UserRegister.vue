<template>
  <div>
    <Navbar2></Navbar2>
    <div class="container p-3 my-3">
      <h1>Register as User</h1>
      <p>Please provide the following information:</p>
      <div class="col-md-6">
        <form @submit.prevent="register">
          <div class="form-group">
            <label for="exampleInputEmail1">Email ID</label>
            <input
              type="email"
              class="form-control"
              id="exampleInputEmail1"
              aria-describedby="emailHelp"
              placeholder="Enter email"
              v-model="email"
              required
            />
            <small id="emailHelp" class="form-text text-muted"
              >We'll never share your email with anyone else.</small
            >
          </div>
          <div class="form-group">
            <label>Username</label>
            <input
              type="text"
              class="form-control"
              placeholder="Enter Username"
              v-model="username"
              required
            />
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
        {{ message }}
      </div>
    </div>
  </div>
</template>

<script>
import Navbar2 from "@/components/Navbar2.vue";
import axios from "axios";

axios.defaults.baseURL = "http://127.0.0.1:8080";

export default {
  data() {
    return {
      email: "",
      password: "",
      username: "",
      message: "",
    };
  },
  methods: {
    isEmail(str) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

      return emailRegex.test(str);
    },
    isUsername(str) {
      return str.length > 0;
    },
    isPassword(str) {
      return str.length > 0;
    },
    async register() {
      if (
        this.isEmail(this.email) &&
        this.isUsername(this.username) &&
        this.isPassword(this.password)
      ) {
        const response = await axios.post("/register/user", {
          username: this.username,
          password: this.password,
          email: this.email,
        });
        console.log(response);
        console.log("submitted");
        this.$router.push("/login");
      } else {
        this.message =
          "The fields are not filled properly. Please check and fill them correctly to register.";
      }
    },
  },
  components: {
    Navbar2,
  },
};
</script>