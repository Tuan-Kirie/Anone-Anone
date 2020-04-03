<template>
    <div class="menu">
        <div class="menu-container">
            <div class="menu-header">
                <span>Фильтры</span>
            </div>
            <div class="menu-content">
                <div class="adult-status">
                    <span>Для взрослых</span>
                    <input type="checkbox" v-model="adult" id="checkbox">
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
                <div class="clear-button">
                    <div class="clear">
                        <span @click="clearFilter">Сбросить все фильтры</span>
                    </div>
                </div>
            </div>
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
        margin-left: 3px;
        align-self: flex-start;
        margin-top: 5px;
        font-size: 16px;
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
        width: 20%;

    }
    .menu-container {
        position: sticky;
        top: 4em;
        margin-top: 75px;
        width: 98%;
        min-height: 260px;
        max-height: 650px;
        background-color: white;
        border: 1px solid #cecece;
        display: flex;
        flex-direction: column;
        text-align: center;
        align-items: center;
        overflow-x: scroll;

        /*overflow-scrolling: auto;*/

    }
    .menu-header {
        margin-top: 10px;
        width: 90%;
        border-bottom: 1px solid #cecece;
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

</style>
<script>
    import axios from 'axios'

    export default {
        name: "Menu",
        data: function () {
            return {
                genres_show: false,
                tags_show: false,
                tags: [],
                genres: [],
                adult: null,
                tags_input: '',
                genres_input: '',
                choosed_tags: [],
                choosed_genres: [],
                choosed_tags_meta: [],
                choosed_genres_meta: [],
            }
        },
        methods: {
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
                this.$emit('clear')
            },
            removeChoosedTags(tag_name) {
                const tag_id = this.choosed_tags_meta.indexOf(tag_name);
                this.choosed_tags_meta.splice(tag_id, 1);
                this.choosed_tags.splice(tag_id, 1);
                this.searchRanobe()
            },
            removeChoosedGenre(genre_name) {
                const genre_id = this.choosed_genres_meta.indexOf(genre_name);
                this.choosed_genres_meta.splice(genre_id, 1);
                this.choosed_genres.splice(genre_id, 1);
                this.searchRanobe()
            },
            getTags() {
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
            getGenres() {
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
            addTagToSearch(tag, tag_name) {
                if (this.choosed_tags.includes(tag) === false) {
                    this.choosed_tags.push(tag);
                    this.choosed_tags_meta.push(tag_name);
                    this.searchRanobe()
                } else {
                    //   Заглушка для надписи
                }

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
                    this.filter = '';
                } else {
                    this.filter = '' + '&adult=' + this.adult;
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


    }
</script>

