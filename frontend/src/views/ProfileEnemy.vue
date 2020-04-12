<template>
    <div class="profile-container">
        <div class="left-column">
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
        <div class="right-column">

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
                username: '',
                email: '',
                img: '',
                birth: '',
            }
        },
        methods: {
            getUserData() {
                let url = 'http://127.0.0.1:8000/another/user/' + this.userID;
                axios.get(url)
                    .then(resp => {
                        console.log(resp.data.user)
                        this.username = resp.data.user.username;
                        this.email = resp.data.user.email;
                        this.birth = resp.data.user.born;
                        this.img += 'http://127.0.0.1:8000' + resp.data.user.img;
                    }).catch(er => {
                    console.log(er)
                })
            }
        },
        mounted() {
            this.getUserData()
        },
    }
</script>

<style scoped>
    .profile-container {
        width: 100%;
        max-width: 100%;
        max-height: 100%;
        overflow: hidden;
        background: #eeeeee;
        height: auto;
        display: grid;
        grid-template-areas: "prof-cont-l prof-cont-r";
        grid-template-columns: 0.3fr 1fr;
        grid-template-rows: 1fr;
        grid-row-gap: 10px;
        padding-bottom: 100px;
        grid-column-gap: 22px;
    }
    .left-column {
        margin-top: 50px;
        grid-area: prof-cont-l;
        box-shadow: 0 0 0 1px #dcdfe6;
        max-width: 300px;
        margin-left: 50px;
        background-color: white;
    }
    .image-container {
        width: 100%;
    }
    .image-container > img {
        width: 100%;
    }
    .right-column {
        margin-top: 50px;
        grid-area: prof-cont-r;
        background-color: white;
        margin-right: 50px;
        box-shadow: 0 0 0 1px #dcdfe6;

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
</style>