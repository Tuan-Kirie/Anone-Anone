<template>
    <div class="blog-wrapper">
        <div class="blog-content">
            <div class="header">
                <span>{{name}}</span>
                <div class="meta-data">
                    <span>{{author_name}}</span>
                    |
                    <span>{{date}}</span>
                </div>
            </div>
            <div class="text-container">
                <div class="text" v-html="text"></div>
            </div>
        </div>
    </div>
</template>

<script>
    import axios from 'axios'

    export default {
        name: "BlogDetail",
        props: ['postId'],
        data() {
            return {
                name: '',
                text: '',
                date: '',
                author: '',
                author_name: '',
            }
        },
        methods: {
            getBlogPostData() {
                let url = 'http://127.0.0.1:8000/blog/' + this.postId;
                axios.get(url)
                    .then(resp => {
                        this.name = resp.data.name;
                        this.text = resp.data.text;
                        this.date = this.normalizeDate(resp.data.published_date);
                        this.author_name = resp.data.author_name;
                        this.author = resp.data.author;
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
            this.getBlogPostData();
        }
    }
</script>

<style scoped>
    .blog-wrapper {
        margin-right: auto;
        margin-left: auto;
        width: 90%;
        margin-top: 25px;
        padding: 25px;
        background-color: white;
        border-radius: 6px;
        border: 1px solid #dadada;
        height: max-content;
    }
    .header {
        width: 100%;
        display: inline-flex;
        justify-content: space-between;
    }
    .header > span {
        font-size: larger;
        font-weight: bold;
    }
    .text {
        margin-top: 25px;
    }

</style>
