<template>
    <div class="ranobe-container">
        <div class="ranobe-left-column">
            <div class="image-container">
                <img class="large-img" v-bind:src="image" alt="">
            </div>
            <router-link class="read-link" :to="{ name: 'RanobeRead', params: { ranobeId: ranobe_id }}">
                <div class="read-button">Читать</div>
            </router-link>
            <div class="dropdown-menu" @click="show_dropdown_content = !show_dropdown_content">
                <span v-if="book_reading_state.length < 1">Добавить в список</span>
                <div v-else>{{book_reading_state}}</div>
                <div class="dropdown-content" v-show="show_dropdown_content">
                    <div class="add-to-planned" @click="addBoodkState('PL')"
                         v-if="book_reading_state !=='Запланировано'">Запланировано
                    </div>
                    <div class="add-to-reade" @click="addBoodkState('RD')" v-if="book_reading_state !== 'Прочитано'">
                        Прочитано
                    </div>
                    <div class="add-to-reading" @click="addBoodkState('RDG')" v-if="book_reading_state !== 'Читаю'">
                        Читаю
                    </div>
                    <div class="remove-from-planned" @click="delBookState" v-if="book_reading_state.length !== 0">
                        Удалить из списка
                    </div>
                </div>
            </div>
        </div>
        <div class="ranobe-main-column">
            <div class="ranobe-info">
                <div class="ranobe-name">
                    <h1>{{this.ranobe_name}}</h1>
                    <h2>{{this.alternate_name}}</h2>
                </div>
                <div class="ranobe-genres" v-if="showCheck(genres)">
                    <h3>Жанры:</h3>
                    <span v-for="genre in this.genres" :key="genre.id">
                        <router-link :to="{name: 'Ranobe', params: {'choosedGenre': {name: genre.name, id: genre.id} }}"> {{genre.name}}</router-link>
                    </span>
                </div>
                <div class="ranobe-description" v-if="showCheck(ranobe_description)">
                    <h3>Описание:</h3>
                    <div class="description-box">{{this.ranobe_description}}</div>
                </div>
                <div class="comment-show-button" v-if="!show_comments" @click="show_comments = true">Загрузить комментарии</div>
                <Comments v-bind:ranobeId="ranobe_id" v-if="show_comments"/>
            </div>
        </div>
        <div class="ranobe-right-column" id="ranobe-right-column-ID">
            <transition name="slide-fade" mode="out-in">
                <div class="add-to-bookmark" @click="addToBookmark" :key="1"
                     v-if="bookmark_on_profile_status !== true">
                    <span>Добавить в закладки</span>
                </div>
                <div class="del-bookmark" @click="delBookmark" :key="2" v-if="bookmark_on_profile_status">
                    <span>Удалить из закладок</span>
                </div>
            </transition>
            <div class="tags-column-container" v-if="tags.length !== 0">
                <div v-if="tags.length > 4">
                    <div class="tags-column" id="show-tags">
                        <h3>Теги</h3>
                        <span v-for="tag in this.tags" :key="tag.id">
                            <router-link :to="{name: 'Ranobe', params: {'choosedTag': {name: tag.name, id: tag.id} }}">
                                {{tag.name}}
                            </router-link>
                        </span>
                    </div>
                    <div class="show-tags" @click="show_full_tags" id="show-tags-b">
                        Показать полностью
                    </div>
                </div>
                <div v-else>
                    <div class="tags-column" style="height: auto">
                        <h3>Теги</h3>
                        <span v-for="tag in this.tags" :key="tag.id">
                            <router-link :to="{name: 'Ranobe', params: {'choosedTag': {name: tag.name, id: tag.id} }}">{{tag.name}}
                            </router-link>
                        </span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
    import axios from 'axios';
    import Comments from "../components/Comments";

    export default {
        name: "RanobeDetail",
        components: {Comments},
        props: ['ranobeId'],
        data() {
            return {
                ranobe_id: this.ranobeId,
                ranobe_name: '',
                ranobe_description: '',
                tags: [],
                genres: [],
                author_name: '',
                publisher_name: '',
                image: '',
                adult_status: '',
                alternate_name: '',
                chapter_next_page: '',
                chapters: [],
                show_comments: false,
                bookmark_on_profile_status: false,
                show_dropdown_content: false,
                show_dropdown_menu: false,
                book_reading_state: '',
            }
        },
        methods: {
            getData() {
                let ranobe_url = 'http://127.0.0.1:8000/ranobe/' + this.ranobe_id;
                axios.get(ranobe_url)
                    .then(resp => {
                        this.ranobe_name = resp.data.name;
                        this.ranobe_description = resp.data.description;
                        this.publisher_name = resp.data.publisher_name;
                        if (resp.data.tags && resp.data.tags.length > 0) {
                            for (let i = 0; i < resp.data.tags.length; i ++)
                                this.tags.push({
                                    'id': resp.data.tags[i],
                                    'name': resp.data.tags_name[i]
                                })
                        }
                        if (resp.data.genres && resp.data.genres.length > 0 ) {
                            for (let j = 0; j < resp.data.genres.length; j ++) {
                                this.genres.push({
                                    'id': resp.data.genres[j],
                                    'name': resp.data.genres_name[j]
                                })
                            }
                        }
                        this.image += ('http://127.0.0.1:8000' + resp.data.image);
                        this.alternate_name = resp.data.alternate_name;
                        this.adult_status = resp.data.adult_status;
                    }).catch(er => console.log(er))
            },
            lazyloadComments() {
                let pos1 = document.documentElement.offsetHeight;
                let pos2 = document.documentElement.scrollTop + window.innerHeight;
                if (pos1 - 30 >= Math.floor(pos2)) {
                    this.show_comments = true
                }
            },
            addToBookmark() {
                if (this.$store.state.token === null) {
                    return alert("Войдите в систему, чтобы добавить ранобэ в список закладок")
                }
                let data = new FormData();
                let bookmark_url = 'http://127.0.0.1:8000/ranobe/' + this.ranobeId + '/bookmark/';
                axios.put(bookmark_url, data, {headers: {'Authorization': "JWT " + this.$store.state.token}})
                    .then(resp => {
                        if (resp.status === 202) {
                            this.bookmark_on_profile_status = true;
                        }
                    }).catch(er => {
                    console.log(er)
                })
            },
            delBookmark() {
                let bookmark_url = 'http://127.0.0.1:8000/ranobe/' + this.ranobeId + '/bookmark/';
                axios.delete(bookmark_url, {headers: {'Authorization': "JWT " + this.$store.state.token}})
                    .then(resp => {
                        if (resp.status === 204) {
                            this.bookmark_on_profile_status = false;
                        }
                    }).catch(er => {
                    console.log(er)
                })
            },
            checkBookmark() {
                let bookmark_url = 'http://127.0.0.1:8000/ranobe/' + this.ranobeId + '/bookmark/';
                axios.get(bookmark_url, {headers: {'Authorization': "JWT " + this.$store.state.token}})
                    .then(resp => {
                        if (resp.data.bookmarked === true) {
                            this.bookmark_on_profile_status = true;
                        }
                    }).catch(er => {
                    console.log(er)
                })
            },
            show_full_tags() {
                let el_show = document.getElementById("show-tags-b");
                let tags_column = document.getElementById("show-tags");
                let column = document.getElementById("ranobe-right-column-ID");
                column.style.position = 'unset';
                tags_column.style.overflow = 'unset';
                tags_column.style.height = 'auto';
                el_show.style.display = 'none';
            },
            addBoodkState(state) {
                if (this.$store.state.token === null) {
                    return alert("Войдите в систему, чтобы добавить ранобэ в свой список")
                }
                let data = new FormData();
                data.append('choice', state);
                let url = 'http://127.0.0.1:8000/ranobe/' + this.ranobe_id + '/readstatus/';
                axios.put(url, data, {headers: {'Authorization': "JWT " + this.$store.state.token}})
                    .then(resp => {
                        if (resp.status === 202) {
                            if (state === "PL") {
                                this.book_reading_state = 'Запланировано'
                            } else if (state === 'RDG') {
                                this.book_reading_state = 'Чтение'
                            } else if (state === 'RD') {
                                this.book_reading_state = 'Прочитано'
                            }
                        }
                    }).catch(er => console.log(er))
            },
            delBookState() {
                let url = 'http://127.0.0.1:8000/ranobe/' + this.ranobe_id + '/readstatus/';
                axios.delete(url, {headers: {'Authorization': "JWT " + this.$store.state.token}})
                    .then(resp => {
                        console.log(resp);
                        this.book_reading_state = '';
                    }).catch(er => console.log(er))
            },
            getBookState() {
                let url = 'http://127.0.0.1:8000/ranobe/' + this.ranobe_id + '/readstatus/';
                axios.get(url, {headers: {'Authorization': "JWT " + this.$store.state.token}})
                    .then(resp => {
                        if (resp.data.read_status === "PL") {
                            this.book_reading_state = 'Запланировано'
                        } else if (resp.data.read_status === 'RDG') {
                            this.book_reading_state = 'Чтение'
                        } else if (resp.data.read_status === 'RD') {
                            this.book_reading_state = 'Прочитано'
                        }
                    })
            },
            showCheck(any_list) {
              if (any_list != null) {
                  if (any_list.length > 0) {
                      return true
                  }
              }
            },

        },
        mounted() {
            //reset scroll position cause window saving before page scroll pos
            window.scrollTo(0,0);
            if (this.$store.state.token !== null)
            {
                this.checkBookmark();
                this.getBookState();
            }
            this.getData();
            window.addEventListener('scroll', this.lazyloadComments);

        }
    }
</script>

<style scoped>
    .comment-show-button {
        margin-top: 70px;
        height: 30px;
        width: 100%;
        border: #3c3c3c 1px solid;
        border-radius: 7px;
        background-color: #FFFFFF;
        font-weight: bold;
        text-align: center;
        padding-top: 10px;
    }
    .comment-show-button:hover, .comment-show-button:active {
        box-shadow: 0 1px 1px 1px rgba(0, 0, 0, .1), 0 0 1px 1px #3c82e6;
    }
    .tags-column {
        margin-top: 20px;
        margin-right: auto;
        margin-left: auto;
        width: 76%;
        border: 1px solid #d8d8d8;
        border-radius: 10px;
        padding: 0 25px 3px 25px;
        display: flex;
        flex-direction: column;
        height: 290px;
        overflow: hidden;
    }
    .tags-column span:last-child {
        padding-bottom: 20px;
    }
    .tags-column > span {
        margin-top: 10px;
        padding-top: 7px;
    }
    .tags-column > span > a {
        text-decoration: none;
        padding: 7px 12px;
        text-align: center;
        line-height: 1;
        white-space: nowrap;
        background-color: hsla(240, 4%, 49%, .07);
        font-size: 1vmax;
        font-weight: 400;
        color: #000;
        margin-top: 7px;
        border-radius: 10px;
    }
    .tags-column > h3 {
        padding-bottom: 7px;
        margin-bottom: 6px;
        border-bottom: 1px solid #cecece;
    }
    .show-tags {
        margin-left: auto;
        margin-right: auto;
        width: 70%;
        height: 20px;
        border-bottom-left-radius: 5px;
        border-bottom-right-radius: 5px;
        text-align: center;
        background-color: hsla(240, 4%, 49%, .07);
        font-size: 1vmax;
        border: 1px solid #d8d8d8;
    }
    .show-tags:last-child {
        padding-bottom: 10px;
    }
    .show-tags:hover, .show-tags:active {
        box-shadow: 0 1px 1px 1px rgba(0, 0, 0, .1), 0 0 1px 1px #3c82e6;
    }

    .ranobe-container {
        background-color: white;
        padding-top: 10px;
        height: auto;
        min-height: 100vh;
        width: 100%;
        justify-self: center;
        display: inline-flex;
    }
    .ranobe-left-column {
        width: 18.75%;
        padding-left: 10px;
        position: sticky;
        height: 500px;
        top: 75px;
    }
    .ranobe-left-column > a {
        text-decoration: none;
    }
    .ranobe-main-column {
        padding-left: 1rem;
        padding-right: 1rem;
        width: 62.5%;
    }
    .ranobe-right-column {
        width: 18.75%;
        position: sticky;
        height: 500px;
        top: 75px;
    }
    .image-container {
    }
    .image-container > img {
        position: relative;
        max-width: 100%;
        min-width: 97%;
        vertical-align: middle;
        background-color: transparent;
        border: 1px solid rgba(0, 0, 0, .1);
        border-radius: 6px;
        cursor: pointer;
    }
    .read-button {
        margin-top: 10px;
        width: 100%;
        height: 30px;
        box-shadow: inset 0 0 0 0 rgba(34, 36, 38, .15);
        background-color: #2185d0;
        color: #FFFFFF;
        text-shadow: none;
        font-size: 1rem;
        border-radius: 5px;
        text-align: center;
        padding-top: 3px;
    }
    .dropdown-menu {
        border: 1px solid hsla(0, 0%, 54.9%, .55);
        padding: 6px 20px;
        text-align: center;
        width: 80%;
        margin-left: 3px;
        font-size: .9em;
        margin-top: 10px;
    }
    .dropdown-menu:active, .dropdown-menu:hover {
        box-shadow: 0 1px 1px 1px rgba(0, 0, 0, .1), 0 0 1px 1px #3c82e6;
    }
    .dropdown-menu > span::before {
        background-image: url("http://127.0.0.1:8080/plus.svg");
        margin-right: 3px;
        content: " ";
        width: 12px;
        display: inline-block;
        background-size: 12px 12px;
        height: 12px;
    }
    .dropdown-menu {
        cursor: pointer;
    }
    .add-to-planned {
        border-top: 1px dotted #3c3c3c;
        padding-top: 10px;
    }
    .dropdown-content > div {
        margin-top: 10px;
        font-weight: bold;
    }
    .dropdown-content > div:hover {
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
    }
    .add-to-bookmark, .del-bookmark {
        border: 1px solid hsla(0, 0%, 54.9%, .55);
        padding: 6px 26px 6px 12px;
        text-align: center;
        width: 80%;
        margin-left: 3px;
        font-size: .9em;
        margin-top: 10px;
        cursor: pointer;
    }
    .add-to-bookmark:hover, .del-bookmark:hover {
        box-shadow: 0 1px 1px 1px rgba(0, 0, 0, .1), 0 0 1px 1px #3c82e6;
    }
    .add-to-bookmark > span:before, .del-bookmark > span:before {
        background-image: url("http://127.0.0.1:8080/bookmark.svg");
        margin-right: 3px;
        vertical-align: middle;
        content: " ";
        width: 12px;
        display: inline-block;
        background-size: 12px 12px;
        height: 12px;
    }
    h1 {
        font-size: 1.71428571rem;
    }
    .ranobe-tags, .ranobe-genres {
        display: inline-flex;
        align-items: center;
        flex-wrap: wrap;
        width: 95%;
    }
    .ranobe-tags > span, .ranobe-genres > span {
        padding-top: 3px;
        display: block;
        width: auto;
        /*max-height: 20px;*/
    }
    .ranobe-tags > span > a, .ranobe-genres > span > a {
        display: inline-block;
        padding: 7px 12px;
        max-height: 20px;
        text-align: center;
        font-size: .9rem;
        font-weight: 400;
        text-decoration: none;
        border-radius: 12px;
        vertical-align: baseline;
        margin-right: 6px;
        color: black;
        white-space: nowrap;
        background-color: hsla(240, 4%, 49%, .07);
    }
    .ranobe-tags > h3, .ranobe-genres > h3 {
        padding-right: 6px;
    }
    .description-box {
        overflow: hidden;
        overflow-wrap: break-word;
    }
    /*.slide-fade-enter-active {*/
    /*    transition: all .3s ease;*/
    /*}*/
    /*.slide-fade-leave-active {*/
    /*    transition: all .3s cubic-bezier(1.0, 0.5, 0.8, 1.0);*/
    /*}*/
    /*.slide-fade-enter, .slide-fade-leave-to*/
    /*    !* .slide-fade-leave-active below version 2.1.8 *!*/
    /*{*/
    /*    !*transform: translateX(15px);*!*/
    /*    opacity: 0;*/
    /*}*/
</style>