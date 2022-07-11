<template>
    <div :key="componentKey">
        <v-row>
            <v-col
                cols="12"
                sm="6"  
                md="3"
                >
                <v-menu
                    v-model="menu"
                    :close-on-content-click="false"
                    :nudge-right="40"
                    transition="scale-transition"
                    offset-y
                    min-width="auto"
                >
                    <template v-slot:activator="{ on, attrs }">
                    <v-text-field
                        v-model="date"
                        label="Select date"
                        prepend-icon="mdi-calendar"
                        readonly
                        v-bind="attrs"
                        v-on="on"
                    ></v-text-field>
                    </template>
                    <v-date-picker
                    v-model="date"
                    :allowed-dates="disableFutureDate"
                    @input="menu = false"
                    ></v-date-picker>
                </v-menu>
            </v-col>
        </v-row>
        <v-row>
            <v-col id="map-wrapper" class="map-wrapper">
                <div class='box' v-show="upHere" :style="{left:xPosition, top:yPosition}">
                    <img class="coverImg" :src=this.imgLink />
                    <div class="text">
                        <div>{{ this.cityName }}</div>
                        <div>{{ this.sunrise }}</div>
                        <div>{{ this.sunset }}</div>
                    </div>
                </div>
            </v-col >
        </v-row>
    </div>
</template>


<style lang="scss">
.map-wrapper {
    display: flex;
    position:relative;
    text-align: center;

  .background {
    fill: transparent;
    pointer-events: all;
  }
  
  .map-layer {
    stroke: #021019;
    stroke-width: 1px;
  }
  .box {
    position: absolute;
    color: black;   
    width: auto;
    height: auto;
  }
  .coverImg {
    max-width: 150px;
    max-height: 100px;
    width: auto;
    height: auto;
    vertical-align: bottom;
  }
  .text {
    background-color: rgba( 255, 255, 255, 0.5 );
  }
}
</style>

<script>
import * as d3 from 'd3'
import axios from 'axios'
import { mapState, mapGetters, mapActions } from 'vuex'

const MAP_GEOJSON = require('../static/data/custom.geo.json');

export default {
  components: {
  },
  props: {
  },
  data() {
    return {
        date: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
        menu: false,
        upHere : false,
        xPosition: 0,
        yPosition: 0,
        imgLink: '',
        cityName: '',
        sunrise: '',
        sunset: '',
        resData: {},
        riseInfo: null,
        setInfo: null,
        province: undefined,
        currentProvince: undefined,
        localSeatInfo : null,
        componentKey: 0,
        svg: null,
        g: null,
        projection: null,
        state: null,
    }
  },
  created() {
  },
  computed: {
    // ...mapState ({
    //     riseInfo: state=>state.sunriseInfo,
    //     setInfo: state=>state.sunsetInfo
    // }),
    // ...mapGetters(["GE_SUNRISE_INFO"]),
    // ...mapGetters(["GE_SUNSET_INFO"]),
  },
//   beforeMount() {
//     this.$store.dispatch('SUNRISE_INFO')
//     this.$store.dispatch('SUNSET_INFO')
//   },
  async mounted() {
    await axios
        .get('/api/rise/')
        .then(response => {
            this.riseInfo = response.data
        })
        .catch(error => {
            console.log(error)
        }),
    await axios
        .get('/api/set/')
        .then(response => {
            this.setInfo = response.data
        })
        .catch(error => {
            console.log(error)
        })

    this.drawMap(); 
    this.drawIcon();
  },
  methods: {
    forceRender() {
        this.componentKey += 1
    },
    
    disableFutureDate(val) {
        return val >= new Date().toISOString().substr(0, 10)
    },

    async getData(lat, lon, standard) {
        const url = `/date/${this.formatDate(this.date)}/lat/${lat}/lon/${lon}/standard/${standard}`
        await axios
            .get(url)
            .then(response => {
                this.sunrise = response.data.sunrise
                this.sunset = response.data.sunset
            })
            .catch(error => {
                    console.log(error)
            })
    },
    formatDate (date) {
        if (!date) return null

        const [year, month, day] = date.split('-')
        return `${year}${month}${day}`
    },

    drawMap() {
        const geojson = MAP_GEOJSON;
        const divWidth = document.getElementById("map-wrapper").clientWidth;
        const width = divWidth
        const height = width * 0.5;

        this.svg = d3
            .select('.map-wrapper')
            .append('svg')
            .attr('width', width)
            .attr('height', height);

        const background = this.svg.append('rect')
            .attr('class', 'background')
            .attr('width', width)
            .attr('height', height)

        this.g = this.svg.append('g');
        const mapLayer = this.g.append('g').classed('map-layer', true);

        this.projection = d3.geoMercator()
            .scale(1)
            .translate([0, 0]); 

        const path = d3.geoPath().projection(this.projection);
        const bounds = path.bounds(geojson);
        const widthScale = (bounds[1][0] - bounds[0][0]) / width; 
        const heightScale = (bounds[1][1] - bounds[0][1]) / height; 
        const scale = 0.95 / Math.max(widthScale, heightScale);
        const xOffset = width/2 - scale * (bounds[1][0] + bounds[0][0]) /2 + 0; 
        const yOffset = height/2 - scale * (bounds[1][1] + bounds[0][1])/2 + 0; 
        const offset = [xOffset, yOffset];
        this.projection.scale(scale).translate(offset);


        const color = d3.scaleLinear()
            .domain([1, 20])
            .clamp(true)
            .range(['#595959', '#595959']);

        function nameLength(d){
            const n = nameFn(d);
            return n ? n.length : 0;
        }

        function nameFn(d){
            return d && d.properties ? d.properties.name : null;
        }

        function fillFn(d){
            return color(nameLength(d));
        }

        mapLayer
            .selectAll('path')
            .data(geojson.features)
            .enter().append('path') 
            .attr('d', path)
            .attr('vector-effect', 'non-scaling-stroke')
            .style('fill', fillFn);
    },
    
    async drawIcon() {
        const riseIcon = this.g.append('g').classed('rise-icon', true);
        const setIcon = this.g.append('g').classed('set-icon', true);

        await riseIcon
        .selectAll('svg')
        .data(this.riseInfo)
        .enter()  
        .append("svg:image")
        .attr("width", 30)
        .attr("height", 30)
        .attr('x' ,  d=> this.projection([d.longitude-2, d.latitude])[0])
        .attr('y' ,  d=> this.projection([d.longitude, d.latitude-(-2)])[1])
        .attr("xlink:href", require("../static/data/sunrise.svg")) 
        .on('mouseover', d =>{
            this.iconOver(d)
        })
        .on('mouseleave', d =>{
            this.upHere = false
        })
        .on('click', d =>{
            this.state = 'rise'
            this.iconClick(this.state)
        })

        await setIcon
        .selectAll('svg')
        .data(this.setInfo)
        .enter()  
        .append("svg:image")
        .attr("width", 30)
        .attr("height", 30)
        .attr('x' ,  d=> this.projection([d.longitude-2, d.latitude])[0])
        .attr('y' ,  d=> this.projection([d.longitude, d.latitude-(-2)])[1])
        .attr("xlink:href", require("../static/data/sunset.svg")) 
        .on('mouseover', d =>{
            this.iconOver(d)
        })
        .on('mouseleave', d =>{
            this.upHere = false
        })
        .on('click', d =>{
            this.state = 'set'
            this.iconClick(this.state)
        })
    },
    iconOver(d) {
        this.upHere = true
        this.xPosition = (d.pageX - 100)  + 'px'
        this.yPosition = (d.pageY - 200)+ 'px'
        const target =  d.target.__data__
        this.imgLink = target.image_link
        this.cityName = target.name
        this.getData(target.latitude, target.longitude, target.standard_time)
    },
    iconClick(s) {
        this.$router.push({ path: "/Place", query: { sunState: s, cityName: this.cityName, date: this.formatDate(this.date)} })
    }
  }
}

</script>