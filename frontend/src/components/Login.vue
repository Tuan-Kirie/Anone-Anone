<template>
    <div class="register-container">
        <div class="register-form-back">
            <form class="register-form" v-if="conf_status===false">
                <span>Регистрация</span>
                <input type="text" v-model="username" placeholder="Введите имя пользователя">
                <input type="password" v-model="password" placeholder="Введите пароль">
                <input type="password" v-model="password_r" placeholder="Повторите пароль" @change="checkPassword">
                <input type="email" v-model="email" placeholder="Введите Email">
                <div class="response-info">
                    <span>{{Password_status.len}}</span>
                    <span>{{Password_status.rep}}</span>
                </div>
                <button @click="register" class="top-button">Регистрация</button>
            </form>
            <form class="login-form" v-else>
                <div class="login-message" >
                    <span>Регистрация прошла успешно</span>
                    <span>Войдите в систему</span>
                </div>
                <form class="login-form">
                    <input type="text" v-model="username" placeholder="Введите имя пользователя">
                    <input type="password" v-model="password" placeholder="Введите пароль">
                    <button @click="login" class="top-button">Вход</button>
                </form>
            </form>
        </div>
    </div>
</template>

<script>
    import axios from 'axios'

    export default {
        name: "Login",
        data() {
            return {
                username: '',
                password: '',
                password_r: '',
                email: '',
                Password_status: {len: '', rep: ''},
                Register_status: '',
                conf_status: false
            }
        },
        methods: {
            register() {
                axios.post('http://127.0.0.1:8000/user/register/', {
                    'username': this.username,
                    'email': this.email,
                    'password': this.password
                })
                    .then(resp => {
                            console.log(resp);
                            this.Register_status = 'Успешная регистрация';
                            this.conf_status = true;
                        }
                    ).catch(er => {
                    console.log(er);
                    this.Register_status = 'Ошибка'
                })
            },
            checkPassword() {
                if (this.password_r !== this.password) {
                    this.Password_status.rep = 'Пароли не совпадают'
                } else {
                    this.Password_status.rep = ''
                }
                if (this.password.length < 8) {
                    this.Password_status.len = 'Длина пароля менее 8'
                } else {
                    this.Password_status.len = ''
                }
            },
            login() {
                this.$store.dispatch('login', {
                    "username": this.username,
                    "password": this.password
                });
                this.login_status = 'Успешно';
            },
        }
    }
</script>

<style scoped>
    .login-form > .top-button {
        margin-top: 16px;
    }
    .register-container {
        display: flex;
        height: 350px;
        align-items: center;
        justify-content: center;
    }
    .login-message {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .login-message > * {
        padding: 3px;
    }
    .login-message > img {
        width: 20%;
        height: 20%;
    }
    .response-info {
        display: flex;
        flex-direction: column;
        font-size: 13px;
    }
    .register-form {
        display: flex;
        flex-direction: column;
        text-align: center;
    }

    .register-form > input {
        border-radius: 3px;
        margin-top: 10px;
        padding: 6px;
        border: 1px solid #acadad;

    }
    .response-info {
        padding: 7px;
    }

    .register-form > button {
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
    .register-form:nth-child(4) {
        margin-top: 11px;
    }
    .register-form > button:hover {
        box-shadow: 0 12px 16px 0 rgba(0, 0, 0, 0.24), 0 17px 50px 0 rgba(0, 0, 0, 0.19);
    }

    .register-form-back {
        padding: 15px;
        background: #FFFFFF;
        border-radius: 5px;
    }
</style>