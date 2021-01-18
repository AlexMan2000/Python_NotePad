

### 绘制条形图

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
  max,
  axisLeft,
  axisBottom,
  format
} from 'd3';

//画布设置
const svg = select('svg');
const height = +svg.attr('height');
const width = +svg.attr('width');

//定义主体渲染函数
const render = data => {
  //从对象数据中的映射关系
  const xValue = d => d.population;
  const yValue = d => d.country; 
 
  //设置画布的margin
  const margin = {top: 20, right: 40, bottom: 70, left: 100};
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;
  
  //(重点)scaleLinear().domain().range()
  const xScale = scaleLinear()
  	.domain([0, max(data, xValue)])
  	.range([0, innerWidth]);
  
  //(重点,用作离散值的映射)scaleBand().domain(list).range()
  //得到yScale构造函数对象（链式编程的结果），映射的值是每一个band的开始坐标位置
  const yScale = scaleBand()
  	.domain(data.map(yValue))
  	.range([0, innerHeight])
  	.padding(.1);//设置每一条bar之间的间距
    
  //svg.append('g')返回一个图元对象,用于生成内部画布,之后所有的图像内容都会在g这个图元中
  //translate(x,y)使得g图元的左上角相对于svg中向右移动x,向下移动y
  const g = svg.append('g')
  	.attr('transform', `translate(${margin.left}, ${margin.top})`);
  
  //将数据绑定在图元上，enter()生成占位符,append()真正的添加上去
  //用attr(属性,映射方法)方法设置每一个图元的属性，d这里指的是每一条数据
  g.selectAll('rect').data(data)
  	.enter().append('rect')
    	//这里要画rect,y属性设置rect的上边为Band的起始坐标,x属性不设置默认是0
  		.attr('y', d => yScale(yValue(d)))
    	//以x,y为左上角起点画出长方形
  		.attr('width', d => xScale(xValue(d)))
  		.attr('height', d => yScale.bandwidth())
    
    
  //设置x轴tick的映射规则,format('.3s')设置3位有效数字
  const xAxisTickFormat = number=>format(".3s")(number).replace('G','B');
  
  //指定x轴整体的规则
  const xAxis = axisBottom(xScale).tickFormat(xAxisTickFormat).tickSize(-innerHeight);
  //指定y轴整体的规则
  const yAxis = axisLeft(yScale);
  
  //在g之下创建g图元，通过调用call方法将规则映射到这些图元上,真正在图上画出来
  const xAxisG = g.append('g').call(xAxis)
  .attr('transform', `translate(0, ${innerHeight})`);
    
    
  //在g之下创建g图元，通过调用call方法将规则映射到这些图元上，真正在图上画出来
  const yAxisG = g.append('g').call(yAxis)
  yAxisG.selectAll(".domain, .tick line").remove();
  
    
  //删除掉左侧的轴线
  xAxisG.select('.domain').remove();
  
  //在xAxisG上加入文字tag,默认添加在xAxisG图元的左上角
  xAxisG.append('text')
              .text('Popularity')
              .attr('y',50)
              .attr('x',innerWidth/2)
              .attr('fill','black')
  
	
  g.append('text').text('Top 10 Most Populous Countries').attr('y',-1)
 
}

//异步回调函数(用于获取数据之后立即进行数据预处理)
//csv('data.csv')IO调取本地数据,本质上是一个Promise对象,then()就是一个回调函数，类似于python线程池/进程池的submit()和add_call_back()
csv('data.csv').then(data => {
    //data就是csv函数获得的数据(是一个经过转换的object对象(Array,里面储存量每一条数据的信息object))
	data.forEach(d => {
    //对每一行数据进行预处理
  	d.population = +d.population * 1000;
  });
  //调用最终的渲染函数
  render(data);
});
```

styles.css

```css
body {
  margin: 0;
  overflow: hidden;
}

rect {
	fill: steelblue;
}

text {
	font-size: 1.5em;
  font-family:sans-serif;
  
}

.tick text{
	fill: #635F5D;

}
```

data.csv

```
country,population
China,1415046
India,1354052
United States,326767
Indonesia,266795
Brazil,210868
Pakistan,200814
Nigeria,195875
Bangladesh,166368
Russia,143965
Mexico,130759
```

Output

![条形图](C:\Users\DELL\Desktop\Python Work\Python Notepad\Python_数据可视化\条形图.png)



重点知识:(链式调用)

```javascript
//构造函数链式调用
function a(){
    this.a = 2;
    this.t = function(){
        console.log("我是t函数")
        return this;
    }
    this.m = function(n){
        console.log("我是m函数,打算修改属性a的值")
        return this;
    }
    this.u = function(){
        console.log("我是u函数,打算为对象设置新的属性")
        this.g = "haha";
        return this;
    }

}
var obj = new a();
obj.t().m().u(); //链式调用
console.log(obj.g)

//对象调用法
var q = {
    a:"haha",
    m:function(){
        console.log("haha")
    }

}
q.m();//普通调用
```









