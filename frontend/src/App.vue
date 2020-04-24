<template>
    <div id="app">
        <div id="nav">
            <div class="logo"></div>
            <router-link to="/" id="home-link">Главная</router-link>
            <router-link to="/ranobe" id="ranobe-link">Ранобэ</router-link>
            <router-link to="/about" id="question-link">FAQ</router-link>
            <div class="login" v-if="!isLoggedIn" @mouseenter="show_login = !show_login"
                 @mouseleave="show_login = !show_login">
                <div class="login-box">
                    <router-link class="login-link" to="/login" id="login-link">Войти</router-link>
                </div>
                <transition name="looklog" mode="out-in">
                    <div class="login-container" id="login-container" v-show="show_login">
                        <div class="login-form-back">
                            <form class="login-form">
                                <input type="text" v-model="username" placeholder="Введите имя пользователя">
                                <input type="password" v-model="password" placeholder="Введите пароль">
                                <div class="response-info">
                                    <span>{{login_status}}</span>
                                </div>
                                <button @click="login" class="top-button">Войти</button>
                                <button @click="register" class="top-button">Регистрация</button>
                            </form>
                        </div>
                    </div>
                </transition>
            </div>
            <div class="profile-mini" @mouseenter="showProfileMenu" @mouseleave="closeProfileMenu" v-else>
                <div class="profile-img">
                    <img v-bind:src="img" class="prof-thumb" alt="">
                    <i class="thumb-ico" id="prof-i">
                        <img src="http://127.0.0.1:8080/prof.svg" alt="">
                    </i>
                </div>
                <div class="hiddenMenu" id="hiddenMenu">
                    <div class="menu-el">
                        <router-link to="/profile" class="hidden-menu-link">Мой профиль</router-link>
                    </div>
                    <div class="menu-el" @click="logout">
                        <a href="#">Выйти</a>
                    </div>
                </div>
            </div>
        </div>
        <router-view/>
        <Footer></Footer>
    </div>
</template>

<style>
    body, html {
        margin: 0;
        min-height: 100%;
        min-width: 100%;
    }
    body {
        background-color: rgba(0, 0, 0, .10);
        font-family: -apple-system, BlinkMacSystemFont, Open Sans, Roboto, Helvetica Neue, Helvetica, sans-serif;
    }
    .looklog-leave-active {
        transition: ease 0.3s;

    }
    .login-container {
        display: flex;
        position: absolute;
        left: -140px;
        align-items: center;
        flex-direction: column;
        justify-content: center;
    }
    .login-form {
        display: flex;
        flex-direction: column;
        text-align: center;
    }
    .login-form > input {
        border-radius: 3px;
        margin-top: 10px;
        padding: 6px;
        border: 1px solid #acadad;
    }
    .response-info {
        padding: 7px;
    }
    .login-form > button {
        background-color: #4CAF50; /* Green */
        border: none;
        color: white;
        border-radius: 5px;
        padding: 7px 12px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        -webkit-transition-duration: 0.4s;
        transition-duration: 0.4s;
    }
    .login-form:nth-child(4) {
        margin-top: 11px;
    }
    .login-form > button:hover {
        box-shadow: 0 12px 16px 0 rgba(0, 0, 0, 0.24), 0 17px 50px 0 rgba(0, 0, 0, 0.19);
    }
    .login-form-back {
        padding: 15px;
        background: #FFFFFF;
        border-radius: 5px;
        transition: ease .5s;
    }
    .hiddenMenu {
        display: none;
        background: #FFFFFF;
        position: absolute;
        width: 130px;
        border-radius: 7px;
        flex-direction: column;
        left: -50px;
    }
    .hiddenMenu > div {
        width: 100%;
        margin-top: 10px;
        padding: 10px;
    }
    .prof-thumb {
        width: 28px;
        height: 28px;
        border-radius: 50%;
    }
    .profile-mini {
        position: absolute;
        right: 66px;
    }
    .thumb-ico {
        margin-left: 15px;
        width: 15px;
        height: 15px;
        transition-duration: 0.3s;
    }
    .profile-img {
        display: flex;
        align-items: center;

    }
    .logo {
        background: url("http://127.0.0.1:8080/logo.png") no-repeat;
        background-size: contain;
        background-position: center;
        width: 103px;
        min-height: 55px;
    }
    .menu-el > a {
        text-decoration: none;
        color: black;
    }
    .menu-el > a:hover {
        text-decoration: underline;
    }
    #nav {
        position: sticky;
        top: 0;
        z-index: 666;
        background: #fff;
        border: none;
        width: 100%;
        height: 60px;
        display: flex;
        font-size: 15px;
        align-items: center;
        justify-content: flex-start;
        border-bottom: solid 1px rgba(0, 0, 0, .32);
    }


    #nav > a {
        color: rgba(0, 0, 0, 0.87);
        text-decoration: none;
        margin-left: 35px;
    }
    #nav > a:hover {
        color: rgba(0, 0, 0, 0.55);
    }
    #ranobe-link::before {
        content: " ";
        display: block;
        background: url("http://127.0.0.1:8080/book.svg"), no-repeat;
        width: 11px;
        height: 11px;
        background-size: 11px;
        float: left;
        margin: 3px 4px 0 0;
    }
    #home-link::before {
        content: " ";
        display: block;
        background: url("http://127.0.0.1:8080/home.svg"), no-repeat;
        width: 11px;
        height: 11px;
        background-size: 11px;
        float: left;
        margin: 3px 4px 0 0;
    }
    #question-link::before {
        content: " ";
        display: block;
        background: url("http://127.0.0.1:8080/question.svg"), no-repeat;
        width: 11px;
        height: 11px;
        background-size: 11px;
        float: left;
        margin: 3px 4px 0 0;
    }
    #login-link::before {
        content: " ";
        display: block;
        background: url("http://127.0.0.1:8080/login.svg"), no-repeat;
        width: 11px;
        height: 11px;
        background-size: 11px;
        float: left;
        margin: 3px 4px 0 0;
    }
    .login {
        position: absolute;
        right: 36px;
    }
    .login-box > a {
        text-decoration: none;
        color: black;
    }
    .login-box > a:hover {
        color: rgba(0, 0, 0, 0.55);
    }
    ::-webkit-scrollbar {
        -webkit-appearance: none;
        width: 10px;
        height: 10px;

    }
    ::-webkit-scrollbar-thumb {
        cursor: pointer;
        border-radius: 5px;
        background: rgba(0, 0, 0, .25);
        transition: color .2s ease;
    }
    ::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0);
        border-radius: 0;
    }
    ::selection {
        background-color: #cce2ff;
        color: rgba(0, 0, 0, .87);
    }
    @media screen and (min-width: 130px) and (max-width:650px) {
        #app {
            overflow: hidden;
        }
        #nav {
            justify-content: flex-start;
        }
        #nav > a {
            margin-left: 3%;
        }
        #nav > *:before {
            display: none;
        }
        .logo {
            display: none;
        }
        .profile-mini {
            right: 3%;
        }
    }
</style>

<script>
    import {mapGetters} from 'vuex'
    import Footer from "./components/Footer";

    export default {
        components: {Footer},
        computed: {
            ...mapGetters([
                'isLoggedIn'
            ]),
        },
        data() {
            return {
                img: localStorage.getItem('profileimg') || '#',
                username: '',
                password: '',
                login_status: '',
                show_login: false,
            }
        },
        methods: {
            login() {
                this.$store.dispatch('login', {
                    "username": this.username,
                    "password": this.password
                });
                this.login_status = 'Успешно';
            },
            register() {
                this.$router.push({name: 'Login'})
            },
            showProfileMenu() {
                let target = document.getElementById('prof-i');
                target.style.transform = 'rotate(90deg)';
                let target_2 = document.getElementById('hiddenMenu');
                target_2.style.display = 'flex'
            },
            closeProfileMenu() {
                let target = document.getElementById('prof-i');
                target.style.transform = 'rotate(0deg)';
                let target_2 = document.getElementById('hiddenMenu');
                target_2.style.display = 'none'
            },
            logout() {
                this.$store.dispatch('logout');
                this.show_login = false;
                this.username = '';
                this.password = '';
                this.login_status = '';
            },
        },
        mounted() {

        }
    }
</script>