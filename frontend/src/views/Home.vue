<template>
    <div class="home-wrapper">
        <div class="home-header">
            <div class="parallax">
                <span>Anone-Anone</span>
                <span>Ранобэ на русском</span>
            </div>
        </div>
        <div class="ranobe-slider-container">

        </div>
        <Blog></Blog>
    </div>
</template>

<script>
    import Blog from "../components/Blog";

    export default {
        name: 'Home',
        components: {Blog}
    }
</script>

<style scoped>
    .home-wrapper {
        min-width: 100%;
        min-height: 100%;
        background: white;
        height: 1300px;
    }
    .home-header {
        width: 100%;
        height: 70vh;
    }
    .parallax {
        background-image: url("http://127.0.0.1:8080/header-bg.jpg");
        height: 100%;
        background-attachment: fixed;
        background-position: center;
        background-repeat: no-repeat;
        background-size: cover;
        max-height: 600px;
        text-align: center;
        vertical-align: middle;
        line-height: 200px;
        display: flex;
        flex-direction: column;
    }
    .parallax > span:first-child {
        padding-top: 50px;
        color: white;
        font-size: 144px;
    }
    .parallax > span {
        color: white;
        font-size: 88px;
    }
</style>