<template>
    <div class="profile-container">
        <div class="info-container">
            <div class="profile-shortcuts">
                <div class="info-column">
                    <div class="profile-statistic">
                        <div class="user-header">
                            <div class="img-container">
                                <img v-bind:src='img' alt="">
                            </div>
                        </div>
                        <div class="block-name">
                            <h3>Информация</h3>
                        </div>
                        <div class="block-info">
                            <span>Имя - {{name}}</span>
                            <span>Дата рождения - {{birth}}</span>
                            <span>Email - {{email}}</span>
                        </div>
                    </div>
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
                </div>
                <div class="profile-info">
                    <div class="profile-menu-list">
                        <div v-bind:class="{active: isActive.bookmarks}" @click="getProfileBookmarks">
                            Закладки
                        </div>
                        <div v-bind:class="{active: isActive.comments}" @click="getProfileComments">
                            Комментарии
                        </div>
                        <div v-bind:class="{active: isActive.ranobe}"
                             @click="isActive.ranobe = true; isActive.bookmarks=false; isActive.comments=false">
                            Список ранобэ
                        </div>
                    </div>
                    <!--                    <h3>Информация</h3>-->
                    <!--                    <div><h4>Последние комментарии: </h4></div>-->
                    <!--                    <div class="comments" v-for="comment in last_comments" :key="comment.id">-->
                    <!--                        <a :href="comment.link"><span>{{comment.text}}</span></a>-->
                    <!--                    </div>-->
                    <div class="content-wrapper">
                        <div class="content-selector" v-if="isActive.bookmarks">
                            <div class="content" v-for="data in content" :key="data.id">
                                <div class="ranobe-container">
                                    <div class="ranobe-img">
                                        <img v-bind:src="data.image" alt="">
                                    </div>
                                    <div class="ranobe-info">
                                        <div class="ranobe-name">{{data.name}}</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="content-selector" v-if="isActive.comments">
                            <div class="comments-container">
                                <div class="comment" v-for="comment in comments" :key="comment.id">
                                    <div class="comment-text">{{comment.text}}</div>
                                    <div class="ranobe-shortcut">{{comments.ranobe_name}}</div>
                                </div>
                            </div>
                        </div>
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
                comments: [],
                planned_books_amount: null,
                reading_books_amount: null,
                read_books_amount: null,
                isActive: {
                    bookmarks: false,
                    comments: false,
                    ranobe: false,
                },
                content: [],
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
                        //DEACTIVATED LAST COMMENTS VIEW
                        // if (resp.data.last_comments.length === 1) {
                        //     this.last_comments.push(resp.data.last_comments[0])
                        // } else if (resp.data.last_comments.length > 1) {
                        //     for (let i = 0; i < resp.data.last_comments.length; i++) {
                        //         resp.data.last_comments[i].link = '?#/ranobe/' + resp.data.last_comments[i].ranobe_id + '/details';
                        //         this.last_comments.push(resp.data.last_comments[i]);
                        //     }
                        // }
                    })
            },
            getProfileBookmarks() {
                this.content = [];
                this.isActive.bookmarks = true;
                this.isActive.ranobe = false;
                this.isActive.comments = false;
                let url = 'http://127.0.0.1:8000/user/profile/bookmark';
                axios.get(url, {headers: {'Authorization': "JWT " + this.token}})
                    .then(
                        resp => {
                            if (resp.data.length === 0) {
                                this.content = ['Нет записей',]
                            } else {
                                for (let b = 0; b !== resp.data.length; b++) {
                                    resp.data[b].image = 'http://127.0.0.1:8000' + resp.data[b].image;
                                    this.content.push(resp.data[b])
                                }
                                console.log(this.content)
                            }
                        }
                    ).catch(er => console.log(er))
            },
            getProfileComments() {
                this.comments = [];
                this.content = [];
                this.isActive.bookmarks = false;
                this.isActive.ranobe = false;
                this.isActive.comments = true;
                let url = 'http://127.0.0.1:8000/user/profile/comments';
                axios.get(url, {headers: {'Authorization': "JWT " + this.token}})
                    .then(
                        resp => {
                            if (resp.data.comments.length > 0) {
                                for (let j = 0; j !== resp.data.comments.length; j++) {
                                    this.comments.push(resp.data.comments[j]);
                                    console.log('F')
                                }
                            } else {
                                this.comments = []
                            }
                        }
                    ).catch(er => {
                    console.log(er)
                })
            },
            normalizeRanobeName(name) {
                //  If name contains char "/" return sliced name else return full name
                if (name.indexOf('/') === -1) {
                    return name
                } else {
                    return name.substring(name.indexOf('/') + 1)
                }
            },
        },
        mounted() {
            this.getProfileData();
            this.getProfileStatistics();
        }
    }
</script>

<style scoped>
    .ranobe-info {
        margin-left: 10px;
        height: 100%;
    }
    .ranobe-img {
        object-fit: cover;
        border-radius: 5px;
        border: 1px solid #cecece;
    }
    .ranobe-img > img {
        display: block;
        height: auto;
        width: 110px;
        max-height: 150px;
    }
    .content {
        margin-top: 10px;
        padding: 0 20px 6px 0;
        width: 90%;
        display: flex;
        height: 150px;
        flex-direction: column;
        border-bottom: 1px solid #e1e1e1;
        cursor: pointer;
    }
    .content:hover {
        -webkit-box-shadow: 4px 0 8px 8px rgba(214, 214, 214, 1);
        -moz-box-shadow: 4px 0 8px 8px rgba(214, 214, 214, 1);
        box-shadow: 4px 0 8px 8px rgba(214, 214, 214, 1);
    }
    .ranobe-container {
        width: 100%;
        height: auto;
        display: flex;
    }
    .profile-container {
        width: 100%;
        max-width: 100%;
        max-height: 100%;
        overflow: hidden;
        background: #eeeeee;
        height: 1300px;
        display: grid;
        /*DELETED header grid are, do not forget*/
        grid-template-areas: "prof-cont prof-cont";
        grid-template-rows: 0.3fr 1fr;
        grid-row-gap: 10px;
        grid-column-gap: 22px;
    }
    .user-header {
        width: 100%;
        max-height: 450px;
        object-fit: cover;
    }
    .img-container > img {
        width: 100%;
        height: auto;
    }
    /*REMOVE HEADER WITH BG*/
    /*.profile-header {*/
    /*    grid-area: header;*/
    /*    min-height: 200px;*/
    /*    background: url('http://127.0.0.1:8080/profile.svg') no-repeat;*/
    /*    background-size: cover;*/
    /*}*/
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
    .profile-menu-list > .active {
        font-weight: bold;
        border-bottom: 2px solid #1b1c1d;
    }
    .profile-menu-list > div:hover {
        border-bottom: 2px solid #1b1c1d;
        color: rgba(0, 0, 0, .95);
    }

</style>