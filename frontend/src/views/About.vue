<template>
    <div>
        <Navbar></Navbar>
        <div class="container my-3">
            <h1 style="text-align:center;">About Us</h1>
            <p>
                We are an electronic library system. Just imagine a library: What does it do? It issues books to people. We do the exact same thing, except we are not a brick and mortar library! We lend books to our users, and they can access it digitally for a given period of one week, after which the book will automatically be returned to us, the library. In other words, we are a digital library management system, or LMS for short.</p>
            <p>
                Like any libarary, we have a wide range of books to offer, of different genres. Be it fiction, non-fiction, popular science, self-help or autobiographies, there is always something here for you. So, why not browse through our collection, and pick and choose? You are free to browse through, and if you like our collection, you can <router-link to="/register/user">sign up</router-link> as a member, and access these books and read them!</p>
            <p>
                We promise that this is a place which avid readers will love! Some of them already call this their second (digital) home!
            </p>
        </div>
    </div>
</template>

<script>
import Navbar from "../components/Navbar.vue";
export default{
    name: 'Home',
    components:{
        Navbar,
    }
}
</script>