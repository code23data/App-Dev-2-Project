<template>
    <div>
        <Navbar2></Navbar2>
        <h2>404</h2>
        <h3>Page not Found</h3>
    </div>
</template>

<script>
    import Navbar2 from '@/components/Navbar2.vue';


    export default {
        data() {
            return {
                email: '',
                password:''
            }
        },
        components: {
            Navbar2,
        },
    }
</script>