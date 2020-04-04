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
                            <div><span>Запланировано: </span> <span>{{planned_books_amount}}</span></div>
                            <div><span>Прочитано: </span> <span>{{read_books_amount}}</span></div>
                            <div><span>Читаю: </span> <span>{{reading_books_amount}}</span></div>
                            <div><span>Всего комментариев: </span> <span>{{comments_amount}}</span></div>
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
                    <div class="profile-menu-list">
                        <div class="profile-bookmarks">
                            Закладки
                        </div>
                        <div class="profile-comments">
                            Комментарии
                        </div>
                        <div class="profile-ranobe-list">
                            Список ранобэ
                        </div>
                    </div>
                    <h3>Информация</h3>
                    <div><h4>Последние комментарии: </h4></div>
                    <div class="comments" v-for="comment in last_comments" :key="comment.id">
                        <a :href="comment.link"><span>{{comment.text}}</span></a>
                    </div>
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
                email: '',
                comments_amount: null,
                last_comments: [],
                planned_books_amount: null,
                reading_books_amount: null,
                read_books_amount: null,
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
                            this.name = resp.data.username;
                            localStorage.setItem('profileimg', this.img)
                        }
                    )
            },
            getProfileStatistics() {
                let url = 'http://127.0.0.1:8000/user/profile/statistic';
                axios.get(url, {headers: {'Authorization': "JWT " + this.token}})
                    .then(resp => {
                        this.comments_amount = resp.data.comments_amount;
                        this.planned_books_amount = resp.data.planned_books_amount;
                        this.reading_books_amount = resp.data.reading_books_amount;
                        this.read_books_amount = resp.data.read_books_amount;
                        if (resp.data.last_comments.length === 1) {
                            this.last_comments.push(resp.data.last_comments[0])
                        } else if (resp.data.last_comments.length > 1) {
                            for (let i = 0; i < resp.data.last_comments.length; i++) {
                                resp.data.last_comments[i].link = '?#/ranobe/' + resp.data.last_comments[i].ranobe_id + '/details';
                                this.last_comments.push(resp.data.last_comments[i]);
                            }
                        }
                    })
            }
        },
        mounted() {
            this.getProfileData();
            this.getProfileStatistics();
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

    .profile-menu-list {
        width: 100%;
        height: 40px;
        border-bottom: 2px solid rgba(34, 36, 38, .15);
        display: flex;
    }

    .profile-menu-list > * {
        cursor: pointer;
        margin-right: 20px;
    }

    .profile-menu-list > div {
        height: 100%;
    }

    .profile-menu-list > div:active, .profile-menu-list > div:hover {
        border-bottom: 2px solid #1b1c1d;
        color: rgba(0, 0, 0, .95);
    }
</style>