<template>
    <div class="home-wrapper">
        <div class="home-header">
            <div class="parallax">
                <span>Anone-Anone</span>
                <span>Ранобэ на русском</span>
            </div>
        </div>
        <div class="ranobe-slider-container">
            <div class="name-header">
                <h3>Последние обновления</h3>
            </div>
            <Slider filter-url="http://127.0.0.1:8000/ranobe"></Slider>
            <div class="name-header">
                <h3>Популярное</h3>
            </div>
            <Slider filter-url="http://127.0.0.1:8000/ranobe/likes"></Slider>
        </div>
        <Blog></Blog>
    </div>
</template>

<script>
    import Blog from "./Blog";
    import Slider from "../components/Slider";

    export default {
        name: 'Home',
        components: {Blog, Slider}
    }
</script>

<style scoped>
    .home-wrapper {
        min-width: 100%;
        min-height: 100%;
        background: white;
        height: max-content;
    }
    .name-header {
        display: inline-flex;
    }
    .name-header > h3 {
        font-size: 1.5em;
        font-weight: 400;
    }
    .name-header > h3:before {
        color: #4183c4;
        content: '#';
        padding-left: 10px;
        padding-right: 5px;
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
        font-size: 100px;
    }
    .parallax > span {
        padding-top: 0;
        color: white;
        font-size: 77px;
    }
    .ranobe-slider-container {
        margin-left: auto;
        margin-right: auto;
        margin-top: 60px;
        width: 100%;
        height: auto;
    }
    @media screen and (min-width: 130px) and (max-width: 650px) {
        .home-header {
            max-height: 44vh;
        }
        .parallax {
            line-height: 50px;
            background-image: url("http://127.0.0.1:8080/header-bg.mini.png");
            background-position: center;
            background-size: cover;
        }
        .parallax > span:first-child {
            margin-top: 20%;
            padding-top: 10px;
            color: white;
            font-size: 44px;
        }
        .parallax > span {
            color: white;
            font-size: 33px;
        }
    }
</style>