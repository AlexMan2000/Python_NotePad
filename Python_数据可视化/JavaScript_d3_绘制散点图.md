index.html

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Bar Chart Learning</title>
    <link rel="stylesheet" href="styles.css">
    <script src="https://unpkg.com/d3@6.3.1/dist/d3.min.js"></script>
  </head>
  <body>
    <svg width="960" height="500">
     
    </svg>
    <script src="bundle.js"></script>
  </body>
</html>
```

index.js

```javascript
import { 
  select, 
  csv, 
  scaleLinear, 
  scaleBand,
  scalePoint,
  max,
  axisLeft,
  axisBottom,
  format,
  extent
} from 'd3';

const svg = select('svg');

const height = +svg.attr('height');
const width = +svg.attr('width');

const render = data => {
  // d.mpg = +d.mpg;
  //   d.cylinders = +d.cylinders;
  //   d.displacement = +d.displacement;
  //   d.horsepower = +d.horsepower;
  //   d.weight = +d.weight;
  //   d.acceleration = +d.acceleration;
  //   d.year = +d.year;
  const xValue = d => d.mpg;
  const yValue = d => d.horsepower; 
  
  //常量参数设置
  const circleRadius = 10;
  const xAxisLabel = 'mpg'
  const yAxisLabel = 'horsePower'
  const title = 'Cars(mpg/horsePower)'
  
  //画布
  const margin = {top: 70, right: 40, bottom: 80, left: 80};
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;
  
  const xScale = scaleLinear()
  	// .domain([min(data,xValue), max(data, xValue)])
  	.domain(extent(data,xValue))
  	.range([0, innerWidth])
  //让tick和画布的边缘对齐
  .nice();
  
  //ScalePoint可以专门用来绘制散点的映射，这里y轴是连续性变量，所以仍然用scaleLinear()
  const yScale = scaleLinear()
  	.domain(extent(data,yValue))
  	.range([0, innerHeight])
  	//让tick和画布的边缘对齐,不设置则默认以x轴数据的最大值和最小值为边缘
  	.nice();
  
  const g = svg.append('g')
  	.attr('transform', `translate(${margin.left}, ${margin.top})`);
   
  
  const xAxisTickFormat = number=>format(".3s")(number).replace('G','B');
  const xAxis = axisBottom(xScale)
    .tickFormat(xAxisTickFormat)
  	//设置衍生距离,负的就是朝原点方向伸展，正值就是往y轴正方向伸展
  	.tickSize(-innerHeight)
  	//把tick远离坐标轴一些
  	.tickPadding(20);
  
  
  const xAxisG = g.append('g').call(xAxis)
  	.attr('transform', `translate(0, ${innerHeight})`);
  
  xAxisG.select('.domain').remove();
	xAxisG.append('text').text(xAxisLabel)
    .attr('y',60)
    .attr('x',innerWidth/2)
    .attr('fill','black')
  	.attr('text-anchor','middle')
  	.attr('class','axis-label')
 
  
  
  const yAxis = axisLeft(yScale)
  	.tickSize(-innerWidth)
  	.tickPadding(10)
  
  const yAxisG = g.append('g').call(yAxis);
  yAxisG.selectAll('.domain').remove();
  yAxisG.append('text').text(yAxisLabel)
    .attr('fill','black')
  	.attr('class','axis-label')
    .attr('transform','rotate(-90)')
  	.attr('y',-40)
  	.attr('x',-innerHeight/2)
  	.attr('text-anchor','middle')
  
  
	g.selectAll('circle').data(data)
  	.enter().append('circle')
  		.attr('cy', d =>yScale(yValue(d)))
  		.attr('cx',d=>xScale(xValue(d)))
  		.attr('r', d => circleRadius)
  g.append('text').text(title)
    .attr('y',-5)
  	.attr('text-anchor','middle')
  	.attr('x',innerWidth/2)
 
}


csv('https://vizhub.com/curran/datasets/auto-mpg.csv')
  .then(data => {
  
	data.forEach(d => {
    //数据预处理，格式转换
  	d.mpg = +d.mpg;
    d.cylinders = +d.cylinders;
    d.displacement = +d.displacement;
    d.horsepower = +d.horsepower;
    d.weight = +d.weight;
    d.acceleration = +d.acceleration;
    d.year = +d.year;
  });
  render(data);
});
```

styles.css

```css
body {
  margin: 0;
  overflow: hidden;
}

circle {
	fill: steelblue;
  opacity:0.5;
}

text {
	font-size: 1.5em;
  font-family:sans-serif;
  
}

.tick text{
	fill: #635F5D;

}

.axis-label {
font-size:2.5em;}
```

OutPut:

![散点图](C:\Users\DELL\Desktop\Python Work\Python Notepad\Python_数据可视化\散点图.png)



ScalePoint用于映射离散点

```javascript
//ScalePoint专门用来绘制散点的映射，仅用于离散值的映射,会将圆心映射到y轴每一个标签的中点
  const yScale = scalePoint()
  	.domain(data.map(yValue))
  	.range([0, innerHeight])
  	.padding(.5);
```

nice()用法

```javascript
const xScale = scaleLinear()
  	.domain([0, max(data, xValue)])
  	.range([0, innerWidth])
  //让tick和画布的边缘对齐,不设置则默认以x轴数据的最大值和最小值为边缘
  .nice();
```

