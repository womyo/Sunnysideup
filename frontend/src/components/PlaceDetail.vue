<template>
    <div>
        <v-parallax height='300' class="placeImg" v-bind:style="{ backgroundImage: `url('${this.imgLink}')` }">
            <h1>{{ this.cityName }}</h1>
        </v-parallax>
        <div class="detail">
            <div class="sunrise">
                <img src="@/static/data/sunrise.svg"/>
                <p>{{ this.sunrise }}</p>
            </div>
            <div class="sunset">
                <img src="@/static/data/sunset.svg"/>
                <p>{{ this.sunset }}</p>
            </div>
        </div>
    </div>
</template>

<style lang="scss">
.placeImg {
    background: no-repeat center;
    background-size: cover;
    text-align: center;
}
.detail {
    text-align: center;
    margin-top: 20px;
    animation: motion 0.5s linear 0s infinite alternate; 
    margin-top: 0;
}
@keyframes motion {
	0% {margin-top: 0px;}
	100% {margin-top: 10px;}
}
.sunrise {
    display: inline-block;
    width: 25%;
    font-size:xx-large;
    font-family:'digital-clock-font';
}
.sunset {
    display: inline-block;
    width: 25%;
    margin-left: 15%;
    font-size:xx-large;
    font-family:'digital-clock-font';
}
</style>

<script>

export default {
    data() {
        return {
            cityName: null,
            cityInfo: null,
            imgLink: null,
            show: false,
        }
    },
    created() {
        this.imgLink = this.$route.query.imgLink
        this.cityName = this.$route.query.cityName
        this.sunrise = this.$route.query.sunrise
        this.sunset = this.$route.query.sunset
        // this.show = true
    },
    methods: {
  }
}
</script>