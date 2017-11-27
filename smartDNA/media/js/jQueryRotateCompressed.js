



<!DOCTYPE html>
<html>
<head>
 <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" >
 <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" >
 
 <meta name="ROBOTS" content="NOARCHIVE">
 
 <link rel="icon" type="image/vnd.microsoft.icon" href="http://www.gstatic.com/codesite/ph/images/phosting.ico">
 
 
 <script type="text/javascript">
 
 
 
 
 var codesite_token = "vR2DS1oxKY1rh47prRfK5GAPjkA:1351066146673";
 
 
 var CS_env = {"profileUrl":"/u/117885600945017564329/","token":"vR2DS1oxKY1rh47prRfK5GAPjkA:1351066146673","assetHostPath":"http://www.gstatic.com/codesite/ph","domainName":null,"assetVersionPath":"http://www.gstatic.com/codesite/ph/17790938420062995905","projectHomeUrl":"/p/jqueryrotate","relativeBaseUrl":"","projectName":"jqueryrotate","loggedInUserEmail":"harpoonsystems@gmail.com"};
 var _gaq = _gaq || [];
 _gaq.push(
 ['siteTracker._setAccount', 'UA-18071-1'],
 ['siteTracker._trackPageview']);
 
 (function() {
 var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
 ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
 (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(ga);
 })();
 
 </script>
 
 
 <title>jQueryRotateCompressed.js - 
 jqueryrotate -
 
 
 jQuery plugin that rotate images (and animate them) by any angle - Google Project Hosting
 </title>
 <link type="text/css" rel="stylesheet" href="http://www.gstatic.com/codesite/ph/17790938420062995905/css/core.css">
 
 <link type="text/css" rel="stylesheet" href="http://www.gstatic.com/codesite/ph/17790938420062995905/css/ph_detail.css" >
 
 
 <link type="text/css" rel="stylesheet" href="http://www.gstatic.com/codesite/ph/17790938420062995905/css/d_sb.css" >
 
 
 
<!--[if IE]>
 <link type="text/css" rel="stylesheet" href="http://www.gstatic.com/codesite/ph/17790938420062995905/css/d_ie.css" >
<![endif]-->
 <style type="text/css">
 .menuIcon.off { background: no-repeat url(http://www.gstatic.com/codesite/ph/images/dropdown_sprite.gif) 0 -42px }
 .menuIcon.on { background: no-repeat url(http://www.gstatic.com/codesite/ph/images/dropdown_sprite.gif) 0 -28px }
 .menuIcon.down { background: no-repeat url(http://www.gstatic.com/codesite/ph/images/dropdown_sprite.gif) 0 0; }
 
 
 
  tr.inline_comment {
 background: #fff;
 vertical-align: top;
 }
 div.draft, div.published {
 padding: .3em;
 border: 1px solid #999; 
 margin-bottom: .1em;
 font-family: arial, sans-serif;
 max-width: 60em;
 }
 div.draft {
 background: #ffa;
 } 
 div.published {
 background: #e5ecf9;
 }
 div.published .body, div.draft .body {
 padding: .5em .1em .1em .1em;
 max-width: 60em;
 white-space: pre-wrap;
 white-space: -moz-pre-wrap;
 white-space: -pre-wrap;
 white-space: -o-pre-wrap;
 word-wrap: break-word;
 font-size: 1em;
 }
 div.draft .actions {
 margin-left: 1em;
 font-size: 90%;
 }
 div.draft form {
 padding: .5em .5em .5em 0;
 }
 div.draft textarea, div.published textarea {
 width: 95%;
 height: 10em;
 font-family: arial, sans-serif;
 margin-bottom: .5em;
 }

 
 .nocursor, .nocursor td, .cursor_hidden, .cursor_hidden td {
 background-color: white;
 height: 2px;
 }
 .cursor, .cursor td {
 background-color: darkblue;
 height: 2px;
 display: '';
 }
 
 
.list {
 border: 1px solid white;
 border-bottom: 0;
}

 
 </style>
</head>
<body class="t4">
<script type="text/javascript">
 window.___gcfg = {lang: 'en'};
 (function() 
 {var po = document.createElement("script");
 po.type = "text/javascript"; po.async = true;po.src = "https://apis.google.com/js/plusone.js";
 var s = document.getElementsByTagName("script")[0];
 s.parentNode.insertBefore(po, s);
 })();
</script>
<div class="headbg">

 <div id="gaia">
 

 <span>
 
 
 
 <a href="#" id="multilogin-dropdown" onclick="return false;"
 ><u><b>harpoonsystems@gmail.com</b></u> <small>&#9660;</small></a>
 
 
 | <a href="/u/117885600945017564329/" id="projects-dropdown" onclick="return false;"
 ><u>My favorites</u> <small>&#9660;</small></a>
 | <a href="/u/117885600945017564329/" onclick="_CS_click('/gb/ph/profile');"
 title="Profile, Updates, and Settings"
 ><u>Profile</u></a>
 | <a href="https://www.google.com/accounts/Logout?continue=http%3A%2F%2Fcode.google.com%2Fp%2Fjqueryrotate%2Fsource%2Fbrowse%2Ftrunk%2FjQueryRotateCompressed.js" 
 onclick="_CS_click('/gb/ph/signout');"
 ><u>Sign out</u></a>
 
 </span>

 </div>

 <div class="gbh" style="left: 0pt;"></div>
 <div class="gbh" style="right: 0pt;"></div>
 
 
 <div style="height: 1px"></div>
<!--[if lte IE 7]>
<div style="text-align:center;">
Your version of Internet Explorer is not supported. Try a browser that
contributes to open source, such as <a href="http://www.firefox.com">Firefox</a>,
<a href="http://www.google.com/chrome">Google Chrome</a>, or
<a href="http://code.google.com/chrome/chromeframe/">Google Chrome Frame</a>.
</div>
<![endif]-->



 <table style="padding:0px; margin: 0px 0px 10px 0px; width:100%" cellpadding="0" cellspacing="0"
 itemscope itemtype="http://schema.org/CreativeWork">
 <tr style="height: 58px;">
 
 
 
 <td id="plogo">
 <link itemprop="url" href="/p/jqueryrotate">
 <a href="/p/jqueryrotate/">
 
 <img src="http://www.gstatic.com/codesite/ph/images/defaultlogo.png" alt="Logo" itemprop="image">
 
 </a>
 </td>
 
 <td style="padding-left: 0.5em">
 
 <div id="pname">
 <a href="/p/jqueryrotate/"><span itemprop="name">jqueryrotate</span></a>
 </div>
 
 <div id="psum">
 <a id="project_summary_link"
 href="/p/jqueryrotate/"><span itemprop="description">jQuery plugin that rotate images (and animate them) by any angle</span></a>
 
 </div>
 
 
 </td>
 <td style="white-space:nowrap;text-align:right; vertical-align:bottom;">
 
 <form action="/hosting/search">
 <input size="30" name="q" value="" type="text">
 
 <input type="submit" name="projectsearch" value="Search projects" >
 </form>
 
 </tr>
 </table>

</div>

 
<div id="mt" class="gtb"> 
 <a href="/p/jqueryrotate/" class="tab ">Project&nbsp;Home</a>
 
 
 
 
 <a href="/p/jqueryrotate/downloads/list" class="tab ">Downloads</a>
 
 
 
 
 
 <a href="/p/jqueryrotate/w/list" class="tab ">Wiki</a>
 
 
 
 
 
 <a href="/p/jqueryrotate/issues/list"
 class="tab ">Issues</a>
 
 
 
 
 
 <a href="/p/jqueryrotate/source/checkout"
 class="tab active">Source</a>
 
 
 
 
 
 
 
 <div class=gtbc></div>
</div>
<table cellspacing="0" cellpadding="0" width="100%" align="center" border="0" class="st">
 <tr>
 
 
 
 
 
 
 
 <td class="subt">
 <div class="st2">
 <div class="isf">
 
 


 <span class="inst1"><a href="/p/jqueryrotate/source/checkout">Checkout</a></span> &nbsp;
 <span class="inst2"><a href="/p/jqueryrotate/source/browse/">Browse</a></span> &nbsp;
 <span class="inst3"><a href="/p/jqueryrotate/source/list">Changes</a></span> &nbsp;
 
 &nbsp;
 
 
 <form action="/p/jqueryrotate/source/search" method="get" style="display:inline"
 onsubmit="document.getElementById('codesearchq').value = document.getElementById('origq').value">
 <input type="hidden" name="q" id="codesearchq" value="">
 <input type="text" maxlength="2048" size="38" id="origq" name="origq" value="" title="Google Code Search" style="font-size:92%">&nbsp;<input type="submit" value="Search Trunk" name="btnG" style="font-size:92%">
 
 
 
 
 
 
 </form>
 <script type="text/javascript">
 
 function codesearchQuery(form) {
 var query = document.getElementById('q').value;
 if (query) { form.action += '%20' + query; }
 }
 </script>
 </div>
</div>

 </td>
 
 
 
 <td align="right" valign="top" class="bevel-right"></td>
 </tr>
</table>


<script type="text/javascript">
 var cancelBubble = false;
 function _go(url) { document.location = url; }
</script>
<div id="maincol"
 
>

 




<div class="expand">
<div id="colcontrol">
<style type="text/css">
 #file_flipper { white-space: nowrap; padding-right: 2em; }
 #file_flipper.hidden { display: none; }
 #file_flipper .pagelink { color: #0000CC; text-decoration: underline; }
 #file_flipper #visiblefiles { padding-left: 0.5em; padding-right: 0.5em; }
</style>
<table id="nav_and_rev" class="list"
 cellpadding="0" cellspacing="0" width="100%">
 <tr>
 
 <td nowrap="nowrap" class="src_crumbs src_nav" width="33%">
 <strong class="src_nav">Source path:&nbsp;</strong>
 <span id="crumb_root">
 
 <a href="/p/jqueryrotate/source/browse/">svn</a>/&nbsp;</span>
 <span id="crumb_links" class="ifClosed"><a href="/p/jqueryrotate/source/browse/trunk/">trunk</a><span class="sp">/&nbsp;</span>jQueryRotateCompressed.js</span>
 
 


 </td>
 
 
 <td nowrap="nowrap" width="33%" align="center">
 <a href="/p/jqueryrotate/source/browse/trunk/jQueryRotateCompressed.js?edit=1"
 ><img src="http://www.gstatic.com/codesite/ph/images/pencil-y14.png"
 class="edit_icon">Edit file</a>
 </td>
 
 
 <td nowrap="nowrap" width="33%" align="right">
 <table cellpadding="0" cellspacing="0" style="font-size: 100%"><tr>
 
 
 <td class="flipper">
 <ul class="leftside">
 
 <li><a href="/p/jqueryrotate/source/browse/trunk/jQueryRotateCompressed.js?r=119" title="Previous">&lsaquo;r119</a></li>
 
 </ul>
 </td>
 
 <td class="flipper"><b>r142</b></td>
 
 </tr></table>
 </td> 
 </tr>
</table>

<div class="fc">
 
 
 
<style type="text/css">
.undermouse span {
 background-image: url(http://www.gstatic.com/codesite/ph/images/comments.gif); }
</style>
<table class="opened" id="review_comment_area"
><tr>
<td id="nums">
<pre><table width="100%"><tr class="nocursor"><td></td></tr></table></pre>
<pre><table width="100%" id="nums_table_0"><tr id="gr_svn142_1"

><td id="1"><a href="#1">1</a></td></tr
><tr id="gr_svn142_2"

><td id="2"><a href="#2">2</a></td></tr
><tr id="gr_svn142_3"

><td id="3"><a href="#3">3</a></td></tr
><tr id="gr_svn142_4"

><td id="4"><a href="#4">4</a></td></tr
><tr id="gr_svn142_5"

><td id="5"><a href="#5">5</a></td></tr
><tr id="gr_svn142_6"

><td id="6"><a href="#6">6</a></td></tr
><tr id="gr_svn142_7"

><td id="7"><a href="#7">7</a></td></tr
><tr id="gr_svn142_8"

><td id="8"><a href="#8">8</a></td></tr
><tr id="gr_svn142_9"

><td id="9"><a href="#9">9</a></td></tr
><tr id="gr_svn142_10"

><td id="10"><a href="#10">10</a></td></tr
><tr id="gr_svn142_11"

><td id="11"><a href="#11">11</a></td></tr
><tr id="gr_svn142_12"

><td id="12"><a href="#12">12</a></td></tr
><tr id="gr_svn142_13"

><td id="13"><a href="#13">13</a></td></tr
><tr id="gr_svn142_14"

><td id="14"><a href="#14">14</a></td></tr
><tr id="gr_svn142_15"

><td id="15"><a href="#15">15</a></td></tr
><tr id="gr_svn142_16"

><td id="16"><a href="#16">16</a></td></tr
><tr id="gr_svn142_17"

><td id="17"><a href="#17">17</a></td></tr
><tr id="gr_svn142_18"

><td id="18"><a href="#18">18</a></td></tr
><tr id="gr_svn142_19"

><td id="19"><a href="#19">19</a></td></tr
><tr id="gr_svn142_20"

><td id="20"><a href="#20">20</a></td></tr
></table></pre>
<pre><table width="100%"><tr class="nocursor"><td></td></tr></table></pre>
</td>
<td id="lines">
<pre><table width="100%"><tr class="cursor_stop cursor_hidden"><td></td></tr></table></pre>
<pre class="prettyprint lang-js"><table id="src_table_0"><tr
id=sl_svn142_1

><td class="source">// VERSION: 2.2 LAST UPDATE: 13.03.2012<br></td></tr
><tr
id=sl_svn142_2

><td class="source">/* <br></td></tr
><tr
id=sl_svn142_3

><td class="source"> * Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php<br></td></tr
><tr
id=sl_svn142_4

><td class="source"> * <br></td></tr
><tr
id=sl_svn142_5

><td class="source"> * Made by Wilq32, wilq32@gmail.com, Wroclaw, Poland, 01.2009<br></td></tr
><tr
id=sl_svn142_6

><td class="source"> * Website: http://code.google.com/p/jqueryrotate/ <br></td></tr
><tr
id=sl_svn142_7

><td class="source"> */<br></td></tr
><tr
id=sl_svn142_8

><td class="source">(function(j){for(var d,k=document.getElementsByTagName(&quot;head&quot;)[0].style,h=[&quot;transformProperty&quot;,&quot;WebkitTransform&quot;,&quot;OTransform&quot;,&quot;msTransform&quot;,&quot;MozTransform&quot;],g=0;g&lt;h.length;g++)void 0!==k[h[g]]&amp;&amp;(d=h[g]);var i=&quot;v&quot;==&quot;\v&quot;;jQuery.fn.extend({rotate:function(a){if(!(0===this.length||&quot;undefined&quot;==typeof a)){&quot;number&quot;==typeof a&amp;&amp;(a={angle:a});for(var b=[],c=0,f=this.length;c&lt;f;c++){var e=this.get(c);if(!e.Wilq32||!e.Wilq32.PhotoEffect){var d=j.extend(!0,{},a),e=(new Wilq32.PhotoEffect(e,d))._rootObj;<br></td></tr
><tr
id=sl_svn142_9

><td class="source">b.push(j(e))}else e.Wilq32.PhotoEffect._handleRotation(a)}return b}},getRotateAngle:function(){for(var a=[],b=0,c=this.length;b&lt;c;b++){var f=this.get(b);f.Wilq32&amp;&amp;f.Wilq32.PhotoEffect&amp;&amp;(a[b]=f.Wilq32.PhotoEffect._angle)}return a},stopRotate:function(){for(var a=0,b=this.length;a&lt;b;a++){var c=this.get(a);c.Wilq32&amp;&amp;c.Wilq32.PhotoEffect&amp;&amp;clearTimeout(c.Wilq32.PhotoEffect._timer)}}});Wilq32=window.Wilq32||{};Wilq32.PhotoEffect=function(){return d?function(a,b){a.Wilq32={PhotoEffect:this};this._img=this._rootObj=<br></td></tr
><tr
id=sl_svn142_10

><td class="source">this._eventObj=a;this._handleRotation(b)}:function(a,b){this._img=a;this._rootObj=document.createElement(&quot;span&quot;);this._rootObj.style.display=&quot;inline-block&quot;;this._rootObj.Wilq32={PhotoEffect:this};a.parentNode.insertBefore(this._rootObj,a);if(a.complete)this._Loader(b);else{var c=this;jQuery(this._img).bind(&quot;load&quot;,function(){c._Loader(b)})}}}();Wilq32.PhotoEffect.prototype={_setupParameters:function(a){this._parameters=this._parameters||{};&quot;number&quot;!==typeof this._angle&amp;&amp;(this._angle=0);&quot;number&quot;===<br></td></tr
><tr
id=sl_svn142_11

><td class="source">typeof a.angle&amp;&amp;(this._angle=a.angle);this._parameters.animateTo=&quot;number&quot;===typeof a.animateTo?a.animateTo:this._angle;this._parameters.step=a.step||this._parameters.step||null;this._parameters.easing=a.easing||this._parameters.easing||function(a,c,f,e,d){return-e*((c=c/d-1)*c*c*c-1)+f};this._parameters.duration=a.duration||this._parameters.duration||1E3;this._parameters.callback=a.callback||this._parameters.callback||function(){};a.bind&amp;&amp;a.bind!=this._parameters.bind&amp;&amp;this._BindEvents(a.bind)},_handleRotation:function(a){this._setupParameters(a);<br></td></tr
><tr
id=sl_svn142_12

><td class="source">this._angle==this._parameters.animateTo?this._rotate(this._angle):this._animateStart()},_BindEvents:function(a){if(a&amp;&amp;this._eventObj){if(this._parameters.bind){var b=this._parameters.bind,c;for(c in b)b.hasOwnProperty(c)&amp;&amp;jQuery(this._eventObj).unbind(c,b[c])}this._parameters.bind=a;for(c in a)a.hasOwnProperty(c)&amp;&amp;jQuery(this._eventObj).bind(c,a[c])}},_Loader:function(){return i?function(a){var b=this._img.width,c=this._img.height;this._img.parentNode.removeChild(this._img);this._vimage=this.createVMLNode(&quot;image&quot;);<br></td></tr
><tr
id=sl_svn142_13

><td class="source">this._vimage.src=this._img.src;this._vimage.style.height=c+&quot;px&quot;;this._vimage.style.width=b+&quot;px&quot;;this._vimage.style.position=&quot;absolute&quot;;this._vimage.style.top=&quot;0px&quot;;this._vimage.style.left=&quot;0px&quot;;this._container=this.createVMLNode(&quot;group&quot;);this._container.style.width=b;this._container.style.height=c;this._container.style.position=&quot;absolute&quot;;this._container.setAttribute(&quot;coordsize&quot;,b-1+&quot;,&quot;+(c-1));this._container.appendChild(this._vimage);this._rootObj.appendChild(this._container);this._rootObj.style.position=<br></td></tr
><tr
id=sl_svn142_14

><td class="source">&quot;relative&quot;;this._rootObj.style.width=b+&quot;px&quot;;this._rootObj.style.height=c+&quot;px&quot;;this._rootObj.setAttribute(&quot;id&quot;,this._img.getAttribute(&quot;id&quot;));this._rootObj.className=this._img.className;this._eventObj=this._rootObj;this._handleRotation(a)}:function(a){this._rootObj.setAttribute(&quot;id&quot;,this._img.getAttribute(&quot;id&quot;));this._rootObj.className=this._img.className;this._width=this._img.width;this._height=this._img.height;this._widthHalf=this._width/2;this._heightHalf=this._height/2;var b=Math.sqrt(this._height*<br></td></tr
><tr
id=sl_svn142_15

><td class="source">this._height+this._width*this._width);this._widthAdd=b-this._width;this._heightAdd=b-this._height;this._widthAddHalf=this._widthAdd/2;this._heightAddHalf=this._heightAdd/2;this._img.parentNode.removeChild(this._img);this._aspectW=(parseInt(this._img.style.width,10)||this._width)/this._img.width;this._aspectH=(parseInt(this._img.style.height,10)||this._height)/this._img.height;this._canvas=document.createElement(&quot;canvas&quot;);this._canvas.setAttribute(&quot;width&quot;,this._width);this._canvas.style.position=&quot;relative&quot;;<br></td></tr
><tr
id=sl_svn142_16

><td class="source">this._canvas.style.left=-this._widthAddHalf+&quot;px&quot;;this._canvas.style.top=-this._heightAddHalf+&quot;px&quot;;this._canvas.Wilq32=this._rootObj.Wilq32;this._rootObj.appendChild(this._canvas);this._rootObj.style.width=this._width+&quot;px&quot;;this._rootObj.style.height=this._height+&quot;px&quot;;this._eventObj=this._canvas;this._cnv=this._canvas.getContext(&quot;2d&quot;);this._handleRotation(a)}}(),_animateStart:function(){this._timer&amp;&amp;clearTimeout(this._timer);this._animateStartTime=+new Date;this._animateStartAngle=this._angle;this._animate()},<br></td></tr
><tr
id=sl_svn142_17

><td class="source">_animate:function(){var a=+new Date,b=a-this._animateStartTime&gt;this._parameters.duration;if(b&amp;&amp;!this._parameters.animatedGif)clearTimeout(this._timer);else{(this._canvas||this._vimage||this._img)&amp;&amp;this._rotate(~~(10*this._parameters.easing(0,a-this._animateStartTime,this._animateStartAngle,this._parameters.animateTo-this._animateStartAngle,this._parameters.duration))/10);this._parameters.step&amp;&amp;this._parameters.step(this._angle);var c=this;this._timer=setTimeout(function(){c._animate.call(c)},10)}this._parameters.callback&amp;&amp;<br></td></tr
><tr
id=sl_svn142_18

><td class="source">b&amp;&amp;(this._angle=this._parameters.animateTo,this._rotate(this._angle),this._parameters.callback.call(this._rootObj))},_rotate:function(){var a=Math.PI/180;return i?function(a){this._angle=a;this._container.style.rotation=a%360+&quot;deg&quot;}:d?function(a){this._angle=a;this._img.style[d]=&quot;rotate(&quot;+a%360+&quot;deg)&quot;}:function(b){this._angle=b;b=b%360*a;this._canvas.width=this._width+this._widthAdd;this._canvas.height=this._height+this._heightAdd;this._cnv.translate(this._widthAddHalf,this._heightAddHalf);this._cnv.translate(this._widthHalf,<br></td></tr
><tr
id=sl_svn142_19

><td class="source">this._heightHalf);this._cnv.rotate(b);this._cnv.translate(-this._widthHalf,-this._heightHalf);this._cnv.scale(this._aspectW,this._aspectH);this._cnv.drawImage(this._img,0,0)}}()};i&amp;&amp;(Wilq32.PhotoEffect.prototype.createVMLNode=function(){document.createStyleSheet().addRule(&quot;.rvml&quot;,&quot;behavior:url(#default#VML)&quot;);try{return!document.namespaces.rvml&amp;&amp;document.namespaces.add(&quot;rvml&quot;,&quot;urn:schemas-microsoft-com:vml&quot;),function(a){return document.createElement(&quot;&lt;rvml:&quot;+a+&#39; class=&quot;rvml&quot;&gt;&#39;)}}catch(a){return function(a){return document.createElement(&quot;&lt;&quot;+<br></td></tr
><tr
id=sl_svn142_20

><td class="source">a+&#39; xmlns=&quot;urn:schemas-microsoft.com:vml&quot; class=&quot;rvml&quot;&gt;&#39;)}}}())})(jQuery);<br></td></tr
></table></pre>
<pre><table width="100%"><tr class="cursor_stop cursor_hidden"><td></td></tr></table></pre>
</td>
</tr></table>

 
<script type="text/javascript">
 var lineNumUnderMouse = -1;
 
 function gutterOver(num) {
 gutterOut();
 var newTR = document.getElementById('gr_svn142_' + num);
 if (newTR) {
 newTR.className = 'undermouse';
 }
 lineNumUnderMouse = num;
 }
 function gutterOut() {
 if (lineNumUnderMouse != -1) {
 var oldTR = document.getElementById(
 'gr_svn142_' + lineNumUnderMouse);
 if (oldTR) {
 oldTR.className = '';
 }
 lineNumUnderMouse = -1;
 }
 }
 var numsGenState = {table_base_id: 'nums_table_'};
 var srcGenState = {table_base_id: 'src_table_'};
 var alignerRunning = false;
 var startOver = false;
 function setLineNumberHeights() {
 if (alignerRunning) {
 startOver = true;
 return;
 }
 numsGenState.chunk_id = 0;
 numsGenState.table = document.getElementById('nums_table_0');
 numsGenState.row_num = 0;
 if (!numsGenState.table) {
 return; // Silently exit if no file is present.
 }
 srcGenState.chunk_id = 0;
 srcGenState.table = document.getElementById('src_table_0');
 srcGenState.row_num = 0;
 alignerRunning = true;
 continueToSetLineNumberHeights();
 }
 function rowGenerator(genState) {
 if (genState.row_num < genState.table.rows.length) {
 var currentRow = genState.table.rows[genState.row_num];
 genState.row_num++;
 return currentRow;
 }
 var newTable = document.getElementById(
 genState.table_base_id + (genState.chunk_id + 1));
 if (newTable) {
 genState.chunk_id++;
 genState.row_num = 0;
 genState.table = newTable;
 return genState.table.rows[0];
 }
 return null;
 }
 var MAX_ROWS_PER_PASS = 1000;
 function continueToSetLineNumberHeights() {
 var rowsInThisPass = 0;
 var numRow = 1;
 var srcRow = 1;
 while (numRow && srcRow && rowsInThisPass < MAX_ROWS_PER_PASS) {
 numRow = rowGenerator(numsGenState);
 srcRow = rowGenerator(srcGenState);
 rowsInThisPass++;
 if (numRow && srcRow) {
 if (numRow.offsetHeight != srcRow.offsetHeight) {
 numRow.firstChild.style.height = srcRow.offsetHeight + 'px';
 }
 }
 }
 if (rowsInThisPass >= MAX_ROWS_PER_PASS) {
 setTimeout(continueToSetLineNumberHeights, 10);
 } else {
 alignerRunning = false;
 if (startOver) {
 startOver = false;
 setTimeout(setLineNumberHeights, 500);
 }
 }
 }
 function initLineNumberHeights() {
 // Do 2 complete passes, because there can be races
 // between this code and prettify.
 startOver = true;
 setTimeout(setLineNumberHeights, 250);
 window.onresize = setLineNumberHeights;
 }
 initLineNumberHeights();
</script>

 
 
 <div id="log">
 <div style="text-align:right">
 <a class="ifCollapse" href="#" onclick="_toggleMeta(this); return false">Show details</a>
 <a class="ifExpand" href="#" onclick="_toggleMeta(this); return false">Hide details</a>
 </div>
 <div class="ifExpand">
 
 
 <div class="pmeta_bubble_bg" style="border:1px solid white">
 <div class="round4"></div>
 <div class="round2"></div>
 <div class="round1"></div>
 <div class="box-inner">
 <div id="changelog">
 <p>Change log</p>
 <div>
 <a href="/p/jqueryrotate/source/detail?spec=svn142&amp;r=120">r120</a>
 by wilq32
 on Mar 13, 2012
 &nbsp; <a href="/p/jqueryrotate/source/diff?spec=svn142&r=120&amp;format=side&amp;path=/trunk/jQueryRotateCompressed.js&amp;old_path=/trunk/jQueryRotateCompressed.js&amp;old=119">Diff</a>
 </div>
 <pre>Updated version number in source files</pre>
 </div>
 
 
 
 
 
 
 <script type="text/javascript">
 var detail_url = '/p/jqueryrotate/source/detail?r=120&spec=svn142';
 var publish_url = '/p/jqueryrotate/source/detail?r=120&spec=svn142#publish';
 // describe the paths of this revision in javascript.
 var changed_paths = [];
 var changed_urls = [];
 
 changed_paths.push('/trunk/jQueryRotate.js');
 changed_urls.push('/p/jqueryrotate/source/browse/trunk/jQueryRotate.js?r\x3d120\x26spec\x3dsvn142');
 
 
 changed_paths.push('/trunk/jQueryRotate3.js');
 changed_urls.push('/p/jqueryrotate/source/browse/trunk/jQueryRotate3.js?r\x3d120\x26spec\x3dsvn142');
 
 
 changed_paths.push('/trunk/jQueryRotateCompressed.js');
 changed_urls.push('/p/jqueryrotate/source/browse/trunk/jQueryRotateCompressed.js?r\x3d120\x26spec\x3dsvn142');
 
 var selected_path = '/trunk/jQueryRotateCompressed.js';
 
 
 function getCurrentPageIndex() {
 for (var i = 0; i < changed_paths.length; i++) {
 if (selected_path == changed_paths[i]) {
 return i;
 }
 }
 }
 function getNextPage() {
 var i = getCurrentPageIndex();
 if (i < changed_paths.length - 1) {
 return changed_urls[i + 1];
 }
 return null;
 }
 function getPreviousPage() {
 var i = getCurrentPageIndex();
 if (i > 0) {
 return changed_urls[i - 1];
 }
 return null;
 }
 function gotoNextPage() {
 var page = getNextPage();
 if (!page) {
 page = detail_url;
 }
 window.location = page;
 }
 function gotoPreviousPage() {
 var page = getPreviousPage();
 if (!page) {
 page = detail_url;
 }
 window.location = page;
 }
 function gotoDetailPage() {
 window.location = detail_url;
 }
 function gotoPublishPage() {
 window.location = publish_url;
 }
</script>

 
 <style type="text/css">
 #review_nav {
 border-top: 3px solid white;
 padding-top: 6px;
 margin-top: 1em;
 }
 #review_nav td {
 vertical-align: middle;
 }
 #review_nav select {
 margin: .5em 0;
 }
 </style>
 <div id="review_nav">
 <table><tr><td>Go to:&nbsp;</td><td>
 <select name="files_in_rev" onchange="window.location=this.value">
 
 <option value="/p/jqueryrotate/source/browse/trunk/jQueryRotate.js?r=120&amp;spec=svn142"
 
 >/trunk/jQueryRotate.js</option>
 
 <option value="/p/jqueryrotate/source/browse/trunk/jQueryRotate3.js?r=120&amp;spec=svn142"
 
 >/trunk/jQueryRotate3.js</option>
 
 <option value="/p/jqueryrotate/source/browse/trunk/jQueryRotateCompressed.js?r=120&amp;spec=svn142"
 selected="selected"
 >/trunk/jQueryRotateCompressed.js</option>
 
 </select>
 </td></tr></table>
 
 
 



 
 </div>
 
 
 </div>
 <div class="round1"></div>
 <div class="round2"></div>
 <div class="round4"></div>
 </div>
 <div class="pmeta_bubble_bg" style="border:1px solid white">
 <div class="round4"></div>
 <div class="round2"></div>
 <div class="round1"></div>
 <div class="box-inner">
 <div id="older_bubble">
 <p>Older revisions</p>
 
 
 <div class="closed" style="margin-bottom:3px;" >
 <img class="ifClosed" onclick="_toggleHidden(this)" src="http://www.gstatic.com/codesite/ph/images/plus.gif" >
 <img class="ifOpened" onclick="_toggleHidden(this)" src="http://www.gstatic.com/codesite/ph/images/minus.gif" >
 <a href="/p/jqueryrotate/source/detail?spec=svn142&r=119">r119</a>
 by wilq32
 on Mar 13, 2012
 &nbsp; <a href="/p/jqueryrotate/source/diff?spec=svn142&r=119&amp;format=side&amp;path=/trunk/jQueryRotateCompressed.js&amp;old_path=/trunk/jQueryRotateCompressed.js&amp;old=86">Diff</a>
 <br>
 <pre class="ifOpened">Some changes to API:
- Added getRotateAngle  function,
- Added stopAnimation,
- Added step parameter,
- Remove some old code (some
...</pre>
 </div>
 
 <div class="closed" style="margin-bottom:3px;" >
 <img class="ifClosed" onclick="_toggleHidden(this)" src="http://www.gstatic.com/codesite/ph/images/plus.gif" >
 <img class="ifOpened" onclick="_toggleHidden(this)" src="http://www.gstatic.com/codesite/ph/images/minus.gif" >
 <a href="/p/jqueryrotate/source/detail?spec=svn142&r=86">r86</a>
 by wilq32
 on Mar 27, 2011
 &nbsp; <a href="/p/jqueryrotate/source/diff?spec=svn142&r=86&amp;format=side&amp;path=/trunk/jQueryRotateCompressed.js&amp;old_path=/trunk/jQueryRotateCompressed.js&amp;old=50">Diff</a>
 <br>
 <pre class="ifOpened">Added MozTransform to use CSS3 in
firefox, removed unused files, some
minor ads changes</pre>
 </div>
 
 <div class="closed" style="margin-bottom:3px;" >
 <img class="ifClosed" onclick="_toggleHidden(this)" src="http://www.gstatic.com/codesite/ph/images/plus.gif" >
 <img class="ifOpened" onclick="_toggleHidden(this)" src="http://www.gstatic.com/codesite/ph/images/minus.gif" >
 <a href="/p/jqueryrotate/source/detail?spec=svn142&r=50">r50</a>
 by wilq32
 on Mar 9, 2011
 &nbsp; <a href="/p/jqueryrotate/source/diff?spec=svn142&r=50&amp;format=side&amp;path=/trunk/jQueryRotateCompressed.js&amp;old_path=/trunk/jQueryRotateCompressed.js&amp;old=43">Diff</a>
 <br>
 <pre class="ifOpened">Fixed small bug when not giving angle
and animateTo</pre>
 </div>
 
 
 <a href="/p/jqueryrotate/source/list?path=/trunk/jQueryRotateCompressed.js&start=120">All revisions of this file</a>
 </div>
 </div>
 <div class="round1"></div>
 <div class="round2"></div>
 <div class="round4"></div>
 </div>
 
 <div class="pmeta_bubble_bg" style="border:1px solid white">
 <div class="round4"></div>
 <div class="round2"></div>
 <div class="round1"></div>
 <div class="box-inner">
 <div id="fileinfo_bubble">
 <p>File info</p>
 
 <div>Size: 6566 bytes,
 20 lines</div>
 
 <div><a href="//jqueryrotate.googlecode.com/svn/trunk/jQueryRotateCompressed.js">View raw file</a></div>
 </div>
 
 </div>
 <div class="round1"></div>
 <div class="round2"></div>
 <div class="round4"></div>
 </div>
 </div>
 </div>


</div>

</div>
</div>

<script src="http://www.gstatic.com/codesite/ph/17790938420062995905/js/prettify/prettify.js"></script>
<script type="text/javascript">prettyPrint();</script>


<script src="http://www.gstatic.com/codesite/ph/17790938420062995905/js/source_file_scripts.js"></script>

 <script type="text/javascript" src="http://www.gstatic.com/codesite/ph/17790938420062995905/js/kibbles.js"></script>
 <script type="text/javascript">
 var lastStop = null;
 var initialized = false;
 
 function updateCursor(next, prev) {
 if (prev && prev.element) {
 prev.element.className = 'cursor_stop cursor_hidden';
 }
 if (next && next.element) {
 next.element.className = 'cursor_stop cursor';
 lastStop = next.index;
 }
 }
 
 function pubRevealed(data) {
 updateCursorForCell(data.cellId, 'cursor_stop cursor_hidden');
 if (initialized) {
 reloadCursors();
 }
 }
 
 function draftRevealed(data) {
 updateCursorForCell(data.cellId, 'cursor_stop cursor_hidden');
 if (initialized) {
 reloadCursors();
 }
 }
 
 function draftDestroyed(data) {
 updateCursorForCell(data.cellId, 'nocursor');
 if (initialized) {
 reloadCursors();
 }
 }
 function reloadCursors() {
 kibbles.skipper.reset();
 loadCursors();
 if (lastStop != null) {
 kibbles.skipper.setCurrentStop(lastStop);
 }
 }
 // possibly the simplest way to insert any newly added comments
 // is to update the class of the corresponding cursor row,
 // then refresh the entire list of rows.
 function updateCursorForCell(cellId, className) {
 var cell = document.getElementById(cellId);
 // we have to go two rows back to find the cursor location
 var row = getPreviousElement(cell.parentNode);
 row.className = className;
 }
 // returns the previous element, ignores text nodes.
 function getPreviousElement(e) {
 var element = e.previousSibling;
 if (element.nodeType == 3) {
 element = element.previousSibling;
 }
 if (element && element.tagName) {
 return element;
 }
 }
 function loadCursors() {
 // register our elements with skipper
 var elements = CR_getElements('*', 'cursor_stop');
 var len = elements.length;
 for (var i = 0; i < len; i++) {
 var element = elements[i]; 
 element.className = 'cursor_stop cursor_hidden';
 kibbles.skipper.append(element);
 }
 }
 function toggleComments() {
 CR_toggleCommentDisplay();
 reloadCursors();
 }
 function keysOnLoadHandler() {
 // setup skipper
 kibbles.skipper.addStopListener(
 kibbles.skipper.LISTENER_TYPE.PRE, updateCursor);
 // Set the 'offset' option to return the middle of the client area
 // an option can be a static value, or a callback
 kibbles.skipper.setOption('padding_top', 50);
 // Set the 'offset' option to return the middle of the client area
 // an option can be a static value, or a callback
 kibbles.skipper.setOption('padding_bottom', 100);
 // Register our keys
 kibbles.skipper.addFwdKey("n");
 kibbles.skipper.addRevKey("p");
 kibbles.keys.addKeyPressListener(
 'u', function() { window.location = detail_url; });
 kibbles.keys.addKeyPressListener(
 'r', function() { window.location = detail_url + '#publish'; });
 
 kibbles.keys.addKeyPressListener('j', gotoNextPage);
 kibbles.keys.addKeyPressListener('k', gotoPreviousPage);
 
 
 }
 </script>
<script src="http://www.gstatic.com/codesite/ph/17790938420062995905/js/code_review_scripts.js"></script>
<script type="text/javascript">
 function showPublishInstructions() {
 var element = document.getElementById('review_instr');
 if (element) {
 element.className = 'opened';
 }
 }
 var codereviews;
 function revsOnLoadHandler() {
 // register our source container with the commenting code
 var paths = {'svn142': '/trunk/jQueryRotateCompressed.js'}
 codereviews = CR_controller.setup(
 {"profileUrl":"/u/117885600945017564329/","token":"vR2DS1oxKY1rh47prRfK5GAPjkA:1351066146673","assetHostPath":"http://www.gstatic.com/codesite/ph","domainName":null,"assetVersionPath":"http://www.gstatic.com/codesite/ph/17790938420062995905","projectHomeUrl":"/p/jqueryrotate","relativeBaseUrl":"","projectName":"jqueryrotate","loggedInUserEmail":"harpoonsystems@gmail.com"}, '', 'svn142', paths,
 CR_BrowseIntegrationFactory);
 
 codereviews.registerActivityListener(CR_ActivityType.REVEAL_DRAFT_PLATE, showPublishInstructions);
 
 codereviews.registerActivityListener(CR_ActivityType.REVEAL_PUB_PLATE, pubRevealed);
 codereviews.registerActivityListener(CR_ActivityType.REVEAL_DRAFT_PLATE, draftRevealed);
 codereviews.registerActivityListener(CR_ActivityType.DISCARD_DRAFT_COMMENT, draftDestroyed);
 
 
 
 
 
 
 
 var initialized = true;
 reloadCursors();
 }
 window.onload = function() {keysOnLoadHandler(); revsOnLoadHandler();};

</script>
<script type="text/javascript" src="http://www.gstatic.com/codesite/ph/17790938420062995905/js/dit_scripts.js"></script>

 
 
 
 <script type="text/javascript" src="http://www.gstatic.com/codesite/ph/17790938420062995905/js/ph_core.js"></script>
 
 
 
 
</div> 

<div id="footer" dir="ltr">
 <div class="text">
 <a href="/projecthosting/terms.html">Terms</a> -
 <a href="http://www.google.com/privacy.html">Privacy</a> -
 <a href="/p/support/">Project Hosting Help</a>
 </div>
</div>
 <div class="hostedBy" style="margin-top: -20px;">
 <span style="vertical-align: top;">Powered by <a href="http://code.google.com/projecthosting/">Google Project Hosting</a></span>
 </div>

 
 


 
 </body>
</html>

