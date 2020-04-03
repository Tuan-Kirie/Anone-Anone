<template>
    <div class="profile-container">
        <div class="profile-header">
            <div class="user-header">
                <div class="img-container">
                    <img v-bind:src='img' alt="">
                </div>
            </div>
        </div>
        <div class="info-container">
            <div class="profile-shortcuts">
                <div class="info-column">
                    <div class="profile-statistic">
                        <div class="block-name">
                            <h3>Статистика</h3>
                        </div>
                        <div class="block-info">
                            <span>4to to</span>
                        </div>
                    </div>
                    <div class="profile-statistic">
                        <div class="block-name">
                            <h3>Информация</h3>
                        </div>
                        <div class="block-info">
                            <span>Имя - {{name}}</span>
                            <span>Дата рождения - {{birth}}</span>
                            <span>Email - {{email}}</span>
                        </div>
                    </div>
                </div>
                <div class="profile-info">
                    <h3>Информация</h3>
                    <span>Имя - {{name}}</span>
                    <span>Дата рождения - {{birth}}</span>
                    <span>Email - {{email}}</span>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import axios from 'axios'
    import {mapState} from "vuex";

    export default {
        name: "Profile",
        computed: {
            ...mapState({
                token: state => state.token
            })
        },
        data() {
            return {
                name: '',
                img: '',
                birth: '',
                email: ''
            }
        },
        methods: {
            getProfileData() {
                axios.get('http://127.0.0.1:8000/user/profile/', {headers: {'Authorization': "JWT " + this.token}})
                    .then(
                        resp => {
                            this.img = resp.data.img;
                            this.birth = resp.data.birth_date;
                            this.email = resp.data.email;
                            this.name = resp.data.username
                            localStorage.setItem('profileimg', this.img)
                        }
                    )
            }
        },
        mounted() {
            this.getProfileData()
        }
    }
</script>

<style scoped>
    .profile-container {
        width: 100%;
        max-width: 100%;
        max-height: 100%;
        overflow: hidden;
        background: #eeeeee;
        height: 1300px;
        display: grid;
        grid-template-areas: "header header" "prof-cont prof-cont";
        grid-template-rows: 0.3fr 1fr;
        grid-row-gap: 10px;
        grid-column-gap: 22px;
    }
    .user-header {
        position: relative;
        bottom: -186px;
        left: 15%;
        display: flex;
        align-items: flex-start;
    }
    .img-container > img {
        height: 150px;
        width: 150px;
        border: solid 3px #FFFFFF;
        border-radius: 50%;
    }
    .profile-header {
        grid-area: header;
        min-height: 200px;
        background: url('http://127.0.0.1:8080/profile.svg') no-repeat;
        background-size: cover;
    }
    .info-container {
        grid-area: prof-cont;


    }
    .profile-shortcuts {
        margin-top: 40px;
        display: flex;
        justify-content: space-around;
    }
    .profile-statistic {
        width: 285px;
        background: #FFFFFF;
        box-shadow: 0 0 0 1px #dcdfe6;
        border-radius: 2px;
        margin-bottom: 15px;
    }
    .block-name {
        overflow: hidden;
        height: 44px;
        margin: 0;
        font-size: 15px;
        font-weight: 600;
        line-height: 1.4;
        text-align: left;
        padding: 0 10px 10px;
        border-bottom: solid 2px #40abe9;
    }
    .info-column {
        width: 285px;
        display: flex;
        flex-direction: column;
    }
    .block-info {
        padding: 10px;
        display: flex;
        flex-direction: column;
    }
    .block-info > * {
        margin-top: 3px;
    }
    .profile-info {
        background: #FFFFFF;
        padding: 20px;
        box-shadow: 0 0 0 1px #dcdfe6;
        border-radius: 2px;
        width: 900px;
    }
</style>