<template>
    <div>
        <div class="comments-container">
            <h3 v-if="comment_status !== 'editing'">Комментарии: </h3>
            <h3 v-else>Редактирование комментария</h3>
            <div v-if="token != null">
                <!--                <textarea v-model="comment_text" placeholder="Оставьте комментарии"-->
                <!--                          class="comment-text-area" id="edit-container"></textarea>-->
                <ckeditor :editor="editor" v-model="comment_text" :config="editorConfig"></ckeditor>

                <div class="comment-buttons" v-if="comment_status !== 'editing'">
                    <button class="send-comment-button" @click="postComment">Отправить</button>
                </div>
                <div class="comment-buttons" v-else>
                    <button class="send-comment-button" @click="editComment">Отредактиовать</button>
                </div>
            </div>
            <div v-else style="padding-bottom: 15px">
                <span style="color: crimson">Войдите в систему, чтобы оставить комментарий</span>
            </div>
            <div class="comments-content" v-for="(comment, index) in comments" :key="index">
                <div class="comments">
                    <div class="comment-author-img">
                        <img v-bind:src="comment.user_img" alt="">
                    </div>
                    <div class="comments-sub-info">
                        <div class="comment-author">
                            <span v-if="comment.user_id === user_id">
                            <router-link to="/profile">{{comment.user}}</router-link>
                            </span>
                            <span v-else>
                                <router-link :to="{ name: 'EnemyProfile', params: { userID: comment.user_id}}">{{comment.user}}</router-link>
                            </span>
                        </div>
                        <div class="comment-t">{{dateNormalize(comment.created_on)}}</div>
                    </div>
                </div>
                <div class="comment-text">
                    <div class="show-edit-menu" v-if="comment.user_id === user_id">
                        <span @click="moveToCommentContainer(comment.id)" v-show="comment.show_status !== true">Редактировать |</span>
                        <span @click="showDeleteMenu(index)" v-show="comment.show_status !== true">Удалить</span>
                        <span v-if="comment.show_status !== false">Удалить комментарии?</span>
                        <span v-if="comment.show_status !== false" @click="deleteComment(comment.id)"
                              style="margin-left: 14px;">ДА</span>
                        <span v-if="comment.show_status !== false" @click="comment.show_status = false"
                              style="margin-left: 14px;">Нет</span>
                    </div>
                    <div v-html="comment.text"></div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import axios from 'axios'
    import {mapState} from "vuex";
    import ClassicEditor from '@ckeditor/ckeditor5-build-classic';


    export default {
        name: "Comments",
        props: ['ranobeId'],
        computed: {
            ...mapState({
                token: state => state.token,
                user_id: state => state.user_id,
                username_pr: state => state.username_pr
            })
        },
        data() {
            return {
                comments: [],
                commentsCounterMes: '',
                url: 'http://127.0.0.1:8000/ranobe/' + this.ranobeId + '/comments/',
                comment_text: '',
                comment_status: 'Комментарии:',
                comment_id: '',
                editor: ClassicEditor,
                editorConfig: {
                    toolbar: ['bold', 'italic', 'link', 'bulletedList', 'numberedList', 'blockQuote'],

                }
            }
        },
        methods: {
            getCommentsOfTitle() {
                axios.get(this.url)
                    .then(resp => {
                        for (let i = 0; i < resp.data.length; i++) {
                            resp.data[i].show_status = false;
                            this.comments.push(resp.data[i]);
                        }
                    }).catch(er => console.log(er))
            },
            postComment() {
                let url_create = this.url + 'post/';
                let data = {'ranobe': this.ranobeId, 'text': this.comment_text};
                axios.post(url_create, data, {headers: {'Authorization': "JWT " + this.token}})
                    .then(resp => {
                        if (resp.status === 201) {
                            this.comment_text = '';
                            this.refreshCommentData()
                        }
                    }).catch(er => console.log(er));
            },
            moveToCommentContainer(comment_id) {
                let container = document.querySelector('#edit-container');
                container.scrollIntoView({behavior: 'smooth', block: 'center',});
                this.comment_status = 'editing';
                this.comment_id = comment_id;
            },
            showDeleteMenu(index) {
                this.comments[index].show_status = true;
            },
            refreshCommentData() {
                axios.get(this.url)
                    .then(resp => {
                        this.comments = [];
                        resp.data[0].show_status = false;
                        for (let i = 0; i < resp.data.length; i++) {
                            resp.data[i].show_status = false;
                            this.comments.push(resp.data[i]);
                        }
                    }).catch(er => console.log(er))
            },
            editComment() {
                let url_edit = this.url + this.comment_id + '/';
                let data = {'text': this.comment_text};
                axios.put(url_edit, data, {headers: {'Authorization': "JWT " + this.token}})
                    .then(resp => {
                        if (resp.status === 200) {
                            this.refreshCommentData()
                        }
                    }).catch(er => {
                    console.log(er)
                });
                this.comment_status = 'Комментарии:';
                this.comment_text = '';
            },
            deleteComment(comment_id) {
                let url_delete = this.url + comment_id + '/';
                console.log(comment_id);
                axios.delete(url_delete, {headers: {'Authorization': "JWT " + this.token}})
                    .then(
                        resp => {
                            if (resp.status === 204) {
                                this.refreshCommentData();
                            }
                        }
                    ).catch(er => {
                    console.log(er)
                })
            },
            dateNormalize(date) {
                let normal = new Date(date);
                const options = {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                    timezone: 'UTC',
                };
                return normal.toLocaleDateString("ru", options)
            },

        },
        mounted() {
            this.getCommentsOfTitle();
            if (this.$store.state.token !== null) {
                this.$store.dispatch('getShortData', localStorage.getItem('token'))
            }

        }
    }
</script>

<style scoped>
    a {
        text-decoration: none;
    }
    .show-edit-menu > span {
        font-size: 13px;
    }
    .show-edit-menu > span:hover {
        cursor: pointer;
        text-decoration: underline;
    }
    .show-edit-menu {
        margin-top: -7px;
        margin-bottom: 8px;
    }
    .comments-container {
        width: 94%;
    }
    .comment-text-area {
        border-radius: 3px;
        padding: 12px 14px;
        width: 100%;
        height: 50px;
    }
    .send-comment-button {
        background-color: #2898af; /* Green */
        border: none;
        color: white;
        border-radius: 5px;
        padding: 8px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin-top: 5px;
        margin-bottom: 24px;
        cursor: pointer;
        -webkit-transition-duration: 0.4s;
        transition-duration: 0.4s;
    }
    .comments {
        display: flex;
        flex-direction: row;
        border-top: #ababab solid 1px;
    }
    .comments-sub-info {
        margin-left: 15px;
        margin-top: 15px;
    }
    .comment-author > span > a {
        font-size: 1em;
        color: rgba(0, 0, 0, .87);
        font-weight: 700;
    }
    .comment-author > span > a:hover {
        text-shadow: 1px 0 #b7b7b7;
    }
    .comment-author-img {
        width: 50px;
        height: 50px;
        margin-top: 15px;
        margin-bottom: 15px;
    }
    .comment-author-img > img {
        display: block;
        width: 50px;
        height: 50px;
        float: left;
        border-radius: 4px;
    }
    .comment-text {
        width: 100%;
        padding: 5px 20px 5px 0;
        margin-bottom: 30px;
        overflow: hidden;
        overflow-wrap: break-word;
    }
</style>