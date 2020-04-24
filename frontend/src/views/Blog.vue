<template>
    <div class="blog-wrapper">
        <div class="blog">
            <div class="post" v-for="post in posts" :key="post.id">
                <div class="post-header">
                    <div class="name">{{post.name}}</div>
                    <div class="meta-data">
                        <div class="author">{{post.author_name}}</div>
                        |
                        <div class="date">{{normalizeDate(post.published_date)}}</div>
                    </div>
                </div>
                <div class="text" v-html="post.text"></div>
                <div class="read-btn-container">
                    <router-link class="blog-link"
                                 :to="{ name: 'BlogDetail', params: { postId: post.id }}">
                        <div class="read-btn">Подробнее</div>
                    </router-link>

                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import axios from 'axios'

    export default {
        name: "Home",
        data() {
            return {
                posts: [],
            }
        },
        methods: {
            getBlogPosts() {
                axios.get('http://127.0.0.1:8000/blog')
                    .then(resp => {
                        this.posts = resp.data
                    }).catch(er => {
                    console.log(er)
                })
            },
            normalizeDate(date) {
                let normal = new Date(date);
                const options = {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                    timezone: 'UTC',
                };
                return normal.toLocaleDateString("ru", options)
            }
        },
        mounted() {
            this.getBlogPosts();
        }
    }
</script>

<style scoped>
    .text {
        padding-top: 20px;
        overflow: hidden;
        word-wrap: break-spaces;
    }
    .meta-data {
        display: inline-flex;
    }
    .name {
        font-weight: bold;
        font-size: larger;
    }
    .read-btn-container {
        width: 100%;
    }
    .read-btn {
        background-color: #4CAF50; /* Green */
        border: none;
        color: white;
        border-radius: 5px;
        padding: 7px 12px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 10px 2px 0 0;
        cursor: pointer;
        -webkit-transition-duration: 0.4s;
        transition-duration: 0.4s;
        float: right;
    }
    .post {
        margin-top: 10px;
        padding: 25px 20px;
        width: 90%;
        display: flex;
        flex-direction: column;
        margin-left: auto;
        margin-right: auto;
        box-shadow: 0 0 0 1px #dcdfe6;
        border-radius: 2px;
    }
    .post-header {
        width: 100%;
        display: inline-flex;
        justify-content: space-between;
    }
    .blog-wrapper {
        width: 100%;
        height: auto;
        /*padding-bottom: 250px;*/
    }
    .blog {
        width: 90%;
        /*height: auto;*/
        margin-top: 50px;
        height: 500px;
        /*background-color: #ececec;*/
        margin-left: auto;
        padding-top: 25px;
        margin-right: auto;
        box-shadow: 0 0 0 1px #dcdfe6;
        border-radius: 2px;
        padding-bottom: 250px;
    }
</style>