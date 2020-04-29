<template>
    <div>
        <div id="menu" class="menu">
            <div class="menu-container">
                <div class="menu-header">
                    <span>Фильтры</span>
                </div>
                <div class="menu-content">
                    <div class="adult-status">
                        <span>Для взрослых</span>
                        <input type="checkbox" v-model="adult" id="checkbox" @change="searchRanobe">
                    </div>
                    <div class="genres">
                        <span @click="getGenres" class="meta-text">Жанры <div class="counter-meta">{{this.choosed_genres.length}}</div></span>
                        <div class="choosed-list">
                            <div class="choosed-meta" v-for="(genre, index) in choosed_genres_meta" :key="index"
                                 @click="removeChoosedGenre(genre)">
                                <span>{{genre}}</span>
                                <img src="http://127.0.0.1:8080/remove.svg" alt="">
                            </div>
                        </div>
                        <transition name="filter">
                            <input type="text" v-show="genres_show" placeholder="Введите жанры"
                                   v-model="genres_input" @input="searchGenres">
                        </transition>
                        <div class="meta-list-container" v-show="genres_show">
                            <div class="genres-list" v-for="genre in genres" :key="genre.id"
                                 @click="addGenreToSearch(genre.id, genre.genre)">{{genre.genre}}
                            </div>
                        </div>
                    </div>
                    <div class="tags">
                    <span @click="getTags" class="meta-text">Теги <div
                            class="counter-meta">{{this.choosed_tags.length}}</div></span>
                        <div class="choosed-list">
                            <div class="choosed-meta" v-for="(tag, index) in choosed_tags_meta" :key="index"
                                 @click="removeChoosedTags(tag)">
                                <span>{{tag}}</span>
                                <img src="http://127.0.0.1:8080/remove.svg" alt="">
                            </div>
                        </div>
                        <transition name="filter">
                            <input type="text" v-show="tags_show" placeholder="Введите теги" v-model="tags_input"
                                   @input="searchTags">
                        </transition>
                        <div class="meta-list-container" v-show="tags_show">
                            <div class="genres-list" v-for="tag in tags" :key="tag.id"
                                 @click="addTagToSearch(tag.id, tag.tag)">
                                {{tag.tag}}
                            </div>
                        </div>
                    </div>
                    <div class="tags">
                        <span @click="getAuthors" class="meta-text">Авторы</span>
                        <div class="choosed-list">
                            <div class="choosed-meta" @click="removeChoosedAuthor"
                                 v-if="this.choosed_author !== null">
                                <span>{{choosed_author.author}}</span>
                                <img src="http://127.0.0.1:8080/remove.svg" alt="">
                            </div>
                        </div>
                        <transition name="filter">
                            <input type="text" v-show="authors_show" placeholder="Введите имя" v-model="author_input"
                                   @input="searchAuthors">
                        </transition>
                        <div class="meta-list-container" v-show="authors_show">
                            <div class="genres-list" v-for="author in authors" :key="author.id"
                                 @click="addAuthorToSearch(author)">
                                {{author.author}}
                            </div>
                        </div>
                    </div>
                    <div class="tags">
                        <span @click="getPublishers" class="meta-text">Издатели</span>
                        <div class="choosed-list">
                            <div class="choosed-meta" @click="removeChoosedPublisher"
                                 v-if="this.choosed_publisher !== null">
                                <span>{{choosed_publisher.publisher}}</span>
                                <img src="http://127.0.0.1:8080/remove.svg" alt="">
                            </div>
                        </div>
                        <transition name="filter">
                            <input type="text" v-show="publishers_show" placeholder="Введите имя"
                                   v-model="publisher_input"
                                   @input="searchPublishers">
                        </transition>
                        <div class="meta-list-container" v-show="publishers_show">
                            <div class="genres-list" v-for="publisher in publishers" :key="publisher.id"
                                 @click="addPublisherToSearch(publisher)">
                                {{publisher.publisher}}
                            </div>
                        </div>
                    </div>
                    <div class="clear-button">
                        <div class="clear">
                            <span @click="clearFilter">Сбросить все фильтры</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="menu-show-button" @click="showHideMenu">
            <span>Фильтры и сортировка</span>
        </div>
    </div>
</template>
<style scoped>
    .choosed-list {
        width: 100%;
    }
    .choosed-meta img {
        content: " ";
        display: block;
        width: 16px;
        height: 16px;
        background-size: 11px;
        float: left;
        margin: 3px 4px 0 0;
    }
    .choosed-meta {
        margin-top: 4px;
        padding-top: 1px;
        width: 100%;
        display: flex;
        justify-content: space-between;
        border-radius: 3px;
        padding-left: 3px;
    }
    .choosed-meta > span {
        white-space: nowrap;
        max-width: 80%;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .choosed-meta:last-child {
        padding-bottom: 10px;
    }
    .choosed-meta:hover {
        background-color: #ff979f;
        cursor: pointer;
    }
    .choosed-meta:nth-child(1) {
        border-top: 1px solid #cecece;
        margin-top: 10px;
    }
    .meta-list-container {
        margin-top: 8px;
        border-top: 1px solid #cecece;
        padding-top: 4px;
    }
    .genres-list {
        border-radius: 4px;
        padding-top: 3px;
    }
    .genres-list:hover {
        background: #dfdfdf;
        cursor: pointer;
    }
    .adult-status > input {
        height: 20px;
        width: 20px;
        background-color: #eee;
        margin-right: 14px;
    }
    .adult-status > input:checked {
        background-color: #2196F3;
    }
    .counter-meta {
        position: relative;
        height: 20px;
        width: 22px;
        margin-right: 15px;
        background: #2185d0;
        border-color: #2185d0;
        color: white;
        border-radius: 3px;
        font-weight: 700;
        text-align: center;
    }
    .meta-text {
        width: 100%;
        display: flex;
        justify-content: space-between;
        cursor: pointer;
    }
    .meta-list-container {
        width: 100%;
        max-height: 300px;
        overflow: scroll;
    }
    .clear-button {
        width: 90%;
        height: 60px;
    }
    .clear {
        margin-left: auto;
        margin-right: auto;
        width: 92%;
        margin-top: 10px;
        border-radius: 5px;
        padding: 3px;
        background: #babbbc;
        cursor: pointer;
    }
    .clear:hover {
        background: rgba(88, 88, 88, 0.8);
    }
    .adult-status {
        margin-top: 15px;
        width: 90%;
        display: flex;
        justify-content: space-between;
        border-bottom: 1px solid #cecece;
        margin-left: 10px;
        padding-bottom: 6px;
        font-size: 15px;
    }
    .genres, .tags {
        display: flex;
        flex-direction: column;
        width: 90%;
        align-items: center;
        border-bottom: 1px solid #cecece;
        padding-bottom: 6px;
    }
    .genres > span, .tags > span {
        font-size: 15px;
        margin-left: 3px;
        align-self: flex-start;
        margin-top: 5px;
        padding: 3px 3px;
    }
    .genres > input, .tags > input {
        width: 100%;
        border-radius: 3px;
        margin-top: 4px;
        border: 1px solid #acadad;
        padding-left: 6px;
        height: 30px;
    }
    .menu-content {
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .menu {
        width: 100%;
        position: sticky;
        top: 7em;
    }
    .menu-container {
        border-radius: 5px;
        margin-top: 75px;
        width: 98%;
        min-height: 230px;
        max-height: 650px;
        background-color: white;
        display: flex;
        flex-direction: column;
        text-align: center;
        align-items: center;
        overflow-x: hidden;
        overflow-y: scroll;
        box-shadow: 0 0 1px 1px rgba(0, 0, 0, 0.1);
    }
    .menu-header {
        margin-top: 10px;
        width: 90%;
        border-bottom: 1px solid #cecece;
        font-weight: bold;
        padding-bottom: 10px;
    }
    .menu-right > span {
    }
    .filter-enter-active {
        transition: all .3s ease;
    }
    .filter-leave-active {
        transition: all .3s cubic-bezier(1.0, 0.5, 0.8, 1.0);
    }
    .filter-enter, .filter-leave-to {
        opacity: 0;
        transform: translateY(14px);
    }
    .menu-show-button {
        display: none;
        width: 0;
    }
    @media screen and (min-width: 130px) and (max-width: 650px) {
        .menu-show-button {
            display: block;
            position: fixed;
            background-color: #e0e1e2;
            text-align: center;
            padding-top: 10px;
            bottom: 0;
            left: 0;
            width: 100%;
            line-height: 1em;
            height: 30px;
            z-index: 668;
            cursor: pointer;
        }
        .menu-show-button > span::before {
            content: " ";
            display: inline-block;
            background: url("http://127.0.0.1:8080/settings.svg"), no-repeat;
            width: 20px;
            height: 20px;
            background-size: 20px;
            margin-right: 5px;
            vertical-align: middle;
        }
        .menu-show-button > span {
            margin-bottom: 20px;
            font-size: 20px;
            color: rgba(0, 0, 0, .6);
            font-weight: 700;
        }
        .menu {
            display: none;
            position: fixed !important;
            left: 0;
            top: 0;
            width: 100%;
            min-width: 150px;
            height: 100%;
            z-index: 667;
        }
        .menu-container {
            margin: 0;
            width: 100%;
            height: 100%;
            max-height: none;
        }
    }
    @media screen and (max-width: 1000px) and (min-width: 650px) {
        .menu {
            width: 100%;
            top: 8.5em;
        }
        .menu-container {
            margin-top: 35px;
        }
    }
    @media screen and (min-width: 1000px) and (max-width: 1300px) {
        .menu {
            width: 100%;
            top: 8.5em;
        }
    }

</style>
<script>
    import axios from 'axios'

    export default {
        name: "Menu",
        props: ['_filter'],
        data: function () {
            return {
                genres_show: false,
                tags_show: false,
                authors_show: false,
                publishers_show: false,
                tags: [],
                genres: [],
                authors: [],
                publishers: [],
                adult: null,
                tags_input: '',
                genres_input: '',
                author_input: '',
                publisher_input: '',
                choosed_tags: [],
                choosed_genres: [],
                choosed_author: null,
                choosed_publisher: null,
                choosed_tags_meta: [],
                choosed_genres_meta: [],
                show_menu: false,
            }
        },
        methods: {
            showHideMenu() {
                let elem = document.getElementById('menu')
                if (this.show_menu) {
                    elem.style.display = 'none'
                    this.show_menu = false
                } else {
                    elem.style.display = 'block'
                    this.show_menu = true
                }
            },
            clearFilter() {
                this.genres_show = false;
                this.tags_show = false;
                this.tags = [];
                this.genres = [];
                this.adult = null;
                this.tags_input = '';
                this.genres_input = '';
                this.choosed_tags = [];
                this.choosed_genres = [];
                this.choosed_genres_meta = [];
                this.choosed_tags_meta = [];
                this.$emit('clear');
                this.$emit('disable');
            },
            removeChoosedTags(tag_name) {
                const tag_id = this.choosed_tags_meta.indexOf(tag_name);
                this.choosed_tags_meta.splice(tag_id, 1);
                this.choosed_tags.splice(tag_id, 1);
                this.searchRanobe()
            },
            removeChoosedAuthor() {
                this.choosed_author = null;
                this.searchRanobe()
            },
            removeChoosedPublisher() {
                this.choosed_publisher = null;
                this.searchRanobe()
            },
            removeChoosedGenre(genre_name) {
                const genre_id = this.choosed_genres_meta.indexOf(genre_name);
                this.choosed_genres_meta.splice(genre_id, 1);
                this.choosed_genres.splice(genre_id, 1);
                this.searchRanobe()
            },
            getTags() {
                 if (this.tags_show === true) {
                    this.tags_show = false
                    this.tags = [];
                    return;
                }
                this.tags = [];
                this.tags_show = !this.tags_show;
                axios.get('http://127.0.0.1:8000/tags/list/')
                    .then(resp => {
                        for (let i = 0; i < resp.data.results.length; i++) {
                            this.tags.push(resp.data.results[i])
                        }
                    }).catch(er => {
                    console.log(er)
                })
            },
            getAuthors() {
                if (this.authors_show === true) {
                    this.authors_show = false
                    this.authors = [];
                    return;
                }
                this.authors = [];
                this.authors_show = !this.authors_show;
                axios.get('http://127.0.0.1:8000/authors/list/')
                    .then(resp => {
                        this.authors = resp.data.results
                    })
            },
            getPublishers() {
                if (this.publishers_show === true) {
                    this.publishers_show = false
                    this.publishers = [];
                    return;
                }
                this.publishers = [];
                this.publishers_show = !this.publishers_show;
                axios.get('http://127.0.0.1:8000/publishers/list/')
                    .then(resp => {
                        this.publishers = resp.data.results
                    })
            },
            getGenres() {
                if (this.genres_show === true) {
                    this.genres_show = false
                    this.genres = [];
                    return;
                }
                this.genres = [];
                this.genres_show = !this.genres_show;
                axios.get('http://127.0.0.1:8000/genres/list/')
                    .then(resp => {
                        for (let i = 0; i < resp.data.results.length; i++) {
                            this.genres.push(resp.data.results[i])
                        }
                    }).catch(er => {
                    console.log(er)
                })
            },
            searchGenres() {
                this.genres = [];
                let search_url = 'http://127.0.0.1:8000/genres/list/?search=' + this.genres_input;
                axios.get(search_url)
                    .then(resp => {
                        for (let i = 0; i < resp.data.results.length; i++) {
                            this.genres.push(resp.data.results[i])
                        }
                    }).catch(er => {
                    console.log(er)
                })
            },
            searchTags() {
                this.tags = [];
                let search_url = 'http://127.0.0.1:8000/tags/list/?search=' + this.tags_input;
                axios.get(search_url)
                    .then(resp => {
                        for (let i = 0; i < resp.data.results.length; i++) {
                            this.tags.push(resp.data.results[i])
                        }
                    }).catch(er => {
                    console.log(er)
                })
            },
            searchAuthors() {
                this.authors = [];
                let search_url = 'http://127.0.0.1:8000/authors/list/?search=' + this.author_input;
                axios.get(search_url)
                    .then(resp => {
                        this.authors = resp.data.results;
                    }).catch(er => {
                    console.log(er)
                })
            },
            searchPublishers() {
                this.publishers = []
                let search_url = 'http://127.0.0.1:8000/publishers/list/?search=' + this.author_input;
                axios.get(search_url)
                    .then(resp => {
                        this.publishers = resp.data.results;
                    }).catch(er => {
                    console.log(er)
                })
            },
            addTagToSearch(tag, tag_name) {
                if (this.choosed_tags.includes(tag) === false) {
                    this.choosed_tags.push(tag);
                    this.choosed_tags_meta.push(tag_name);
                    this.searchRanobe()
                } else {
                    //   Заглушка для надписи
                }
            },
            addAuthorToSearch(author) {
                this.choosed_author = author
                this.searchRanobe()
            },
            addPublisherToSearch(publisher) {
                this.choosed_publisher = publisher
                this.searchRanobe()
            },
            addGenreToSearch(genre, genre_name) {
                if (this.choosed_genres.includes(genre) === false) {
                    this.choosed_genres.push(genre);
                    this.choosed_genres_meta.push(genre_name);
                    this.searchRanobe();
                } else {
                    //   Заглушка для надписи
                }
            },
            searchRanobe() {
                let ranobes = [];
                let filter = '';
                if (this.adult === null) {
                    filter = '';
                } else {
                    filter = '' + '&adult=' + this.adult;
                }
                // Урл обратабывает нормально, если на 1 элем оставить &
                if (this.choosed_tags.length > 1) {
                    for (let x = 0; x < this.choosed_tags.length; x++) {
                        filter += '&tags=' + this.choosed_tags[x]
                    }
                } else if (this.choosed_tags.length === 1) {
                    filter += '&tags=' + this.choosed_tags[0]
                }
                if (this.choosed_genres.length > 1) {

                    for (let x = 0; x < this.choosed_genres.length; x++) {
                        filter += '&genres=' + this.choosed_genres[x]
                    }
                } else if (this.choosed_genres.length === 1) {
                    filter += '&genres=' + this.choosed_genres[0]
                }
                if (this.choosed_author !== null) {
                    filter += '&author=' + this.choosed_author.id
                }
                if (this.choosed_publisher !== null) {
                    filter += '&publisher=' + this.choosed_publisher.id
                }
                let search_url = 'http://127.0.0.1:8000/ranobe/?' + filter;
                axios.get(search_url)
                    .then(resp => {
                        for (let i = 0; i < resp.data.results.length; i++) {
                            ranobes.push(resp.data.results[i])
                        }
                    }).catch(er => console.log(er));
                this.$emit('update', ranobes)
            },
        },
        mounted() {
            if (this._filter.tag !== undefined) {
                this.choosed_tags.push(this._filter.tag.id);
                this.choosed_tags_meta.push(this._filter.tag.name);
                this.searchRanobe();
            }
            if (this._filter.genre !== undefined) {
                this.choosed_genres.push(this._filter.genre.id);
                this.choosed_genres_meta.push(this._filter.genre.name);
                this.searchRanobe();
            }
        }


    }
</script>

