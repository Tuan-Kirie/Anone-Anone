<template>
    <div class="profile-container">
        <div class="left-column">
            <div class="fixed-container">
                <div class="image-container">
                    <img :src="img" alt="">
                </div>
                <div class="block-name">
                    <h3>Информация</h3>
                </div>
                <div class="block-info">
                    <span>Имя - {{username}}</span>
                    <span>Дата рождения - {{birth}}</span>
                    <span>Email - {{email}}</span>
                </div>
            </div>
        </div>
        <div class="right-column">
            <div class="ranobes-container">
                <span id="ranobe-list-b" class="elem-name">Список ранобэ</span>
                <div class="ranobe-filter">
                    <div v-bind:class="{active: isActive.all}" @click="getMarkedRanobes(); contentActivator(0)">
                        <span>Все</span></div>
                    <div v-bind:class="{active: isActive.planned}" @click="getMarkedRanobes('PL'); contentActivator(1)">
                        <span>Запланировано</span></div>
                    <div v-bind:class="{active: isActive.reading}"
                         @click="getMarkedRanobes('RDG'); contentActivator(2)">
                        <span>Читаю</span></div>
                    <div v-bind:class="{active: isActive.read}" @click="getMarkedRanobes('RD'); contentActivator(3)">
                        <span>Прочитано</span>
                    </div>
                </div>
                <div class="ranobe-content-list">
                    <div class="content" v-for="data in content" :key="data.id">
                        <router-link class="ran-link"
                                     :to="{ name: 'RanobeDetail', params: { ranobeId: data.id }}">
                            <div class="ranobe-container">
                                <div class="ranobe-img">
                                    <img v-bind:src="appendTrueImgUrl(data.image)" alt="">
                                </div>
                                <div class="ranobe-info">
                                    <div class="ranobe-name"><span>{{data.name}}</span></div>
                                </div>
                            </div>
                        </router-link>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import axios from 'axios'

    export default {
        name: "User",
        props: ['userID'],
        data() {
            return {
                isActive: {
                    all: '',
                    planned: '',
                    reading: '',
                    read: ''
                },
                username: '',
                email: '',
                img: '',
                birth: '',
                content: [],
            }
        },
        methods: {
            getUserData() {
                let url = 'http://127.0.0.1:8000/another/user/' + this.userID;
                axios.get(url)
                    .then(resp => {
                        this.username = resp.data.user.username;
                        this.email = resp.data.user.email;
                        this.birth = resp.data.user.born;
                        this.img += 'http://127.0.0.1:8000' + resp.data.user.img;
                    }).catch(er => {
                    console.log(er)
                })
            },
            getUserMarkedRanobes() {
                let url = 'http://127.0.0.1:8000/another/user/' + this.userID + '/ranobes';
                axios.get(url)
                    .then(resp => {
                        this.content = resp.data.ranobes
                    })
            },
            appendTrueImgUrl(media_url) {
                return 'http://127.0.0.1:8000' + media_url;
            },
            getMarkedRanobes(filter) {
                this.content = [];
                let url = 'http://127.0.0.1:8000/another/user/' + this.userID + '/ranobes';
                if (filter !== undefined) {
                    url += `?Rtype=${filter}`;
                } else if (this.isActive.read === true
                    || this.isActive.planned === true
                    || this.isActive.reading === true) {
                    this.isActive.all = false
                }
                axios.get(url)
                    .then(resp => {
                        if (resp.data.ranobes.length > 0) {
                            for (let j = 0; j !== resp.data.ranobes.length; j++) {
                                this.appendTrueImgUrl(resp.data.ranobes[j].image);
                                this.content.push(resp.data.ranobes[j]);
                            }
                        }
                    })
            },
            contentActivator(type) {
                this.isActive.all = (type === 0);
                this.isActive.planned = (type === 1);
                this.isActive.reading = (type === 2);
                this.isActive.read = (type === 3);

            },
        },
        mounted() {
            this.getUserData();
            this.getUserMarkedRanobes();
            this.isActive.all = true
        },
    }
</script>

<style scoped>
    a {
        text-decoration: none;
    }
    .ranobe-name {
        color: black;
        font-size: larger;
    }
    .ranobe-container {
        width: 100%;
        height: auto;
        display: flex;
    }
    .elem-name {
        display: block;
        padding: 25px 0 10px 25px;
        font-size: larger;
    }
    .elem-name:before {
        color: #4183c4;
        content: '#';
        padding-left: 10px;
        padding-right: 5px;
    }
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
    .profile-container {
        width: 100%;
        max-width: 100%;
        max-height: 100%;
        overflow: hidden;
        background: #eeeeee;
        height: auto;
        display: flex;
        justify-content: center;
        /*display: grid;*/
        /*grid-template-areas: "prof-cont-l prof-cont-r";*/
        /*grid-template-columns: 0.3fr 1fr;*/
        /*grid-template-rows: 1fr;*/
        /*grid-row-gap: 10px;*/
        padding-bottom: 100px;
        /*grid-column-gap: 22px;*/
    }
    .left-column {
        height: auto;
        margin-top: 50px;
        /*grid-area: prof-cont-l;*/
        box-shadow: 0 0 0 1px #dcdfe6;
        max-width: 300px;
        margin-left: 50px;
        background-color: white;
        max-height: 560px;
    }
    .fixed-container {
        height: 500px;
        position: sticky;
    }
    .image-container {
        width: 100%;
    }
    .image-container > img {
        width: 100%;
    }
    .right-column {
        margin: 50px;
        /*grid-area: prof-cont-r;*/
        background-color: white;
        max-width: 900px;
        box-shadow: 0 0 0 1px #dcdfe6;
        padding-bottom: 50px;
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
    .block-info {
        padding: 10px;
        display: flex;
        flex-direction: column;
    }
    .block-info > * {
        margin-top: 3px;
    }
    .ranobe-filter {
        margin-top: 10px;
        display: inline-flex;
        width: 100%;
        justify-content: space-around;
    }
    .ranobe-filter > div {
        width: 150px;
        line-height: 30px;
        height: 30px;
        border-radius: 4px;
        cursor: pointer;
        /*background-color: #e5e5e5;*/
        text-align: center;
        border: 1px solid #e5e5e5;
    }
    .ranobe-filter > div.active {
        box-shadow: 0 1px 1px 1px rgba(0, 0, 0, .1), 0 0 1px 1px #3c82e6;
    }
    .content {
        margin-top: 30px;
        margin-left: auto;
        margin-right: auto;
        padding: 0 20px 6px 0;
        width: 90%;
        display: flex;
        height: 150px;
        flex-direction: column;
        border-bottom: 1px solid #e1e1e1;
        cursor: pointer;
        border-radius: 5px;
    }
    .content:hover {
        background-color: #f6f6f6;
        box-shadow: 0 0 0 1px rgba(214, 214, 214, 1);
    }
    @media screen and (min-width: 130px) and (max-width: 650px) {
        .left-column, .right-column {
            margin-left: auto;
            margin-right: auto;
        }

        .ranobe-filter > * {
            font-size: 12px;
        }
        .ranobe-filter > div {
            width: auto;
            padding: 0 10px 0 10px;
        }
        .profile-menu-list > div {
            text-align: center;
            line-height: 50px;
        }
        .profile-container {
            display: flex;
            flex-direction: column;
        }
        .block-info {
            background-color: white;
            padding-bottom: 15px;
        }
        .right-column {
            margin-top: 100px;
            padding-bottom: 100px;
        }
        .content {
            overflow: hidden;
        }
        .ranobe-name {
            padding: 0 5px 0 5px;
            font-size: 13px;
        }
        .ranobe-container {
            overflow: hidden;
            max-height: 100%;
        }
        .content > a {
            max-height: 100%;
            overflow: hidden;
        }
        .ranobe-info {
            max-height: 100%;
            overflow: hidden;
        }
        .elem-name {
            padding-left: 10px;
        }
    }
    @media screen and (min-width: 750px) and (max-width: 1200px) {
        .right-column {
            max-width: 50%;

        }
        .ranobe-name {
            font-size: 13px;
        }
        .ranobe-filter {
            font-size: 0.9rem;
        }
        .ranobe-filter > div { 
            width: auto;
            padding: 0 10px 0 10px;
        }
    }
</style>