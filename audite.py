"""
Taylor Seale & Iheanyi Ekechukwu
"""

import cherrypy
import os
from mako.template import Template
from mako.lookup import TemplateLookup

header = """<!DOCTYPE html>
				<html lang="en">
				  <head>
				    <meta charset="utf-8">
				    <title>Audite... Listen Up</title>
				    <meta name="viewport" content="width=device-width, initial-scale=1.0">
				    <meta name="description" content="Paradigms Project">
				    <meta name="author" content="Taylor Seale & Iheanyi Ekechukwu">

				    <!-- Le styles -->
				    <link href="//netdna.bootstrapcdn.com/twitter-bootstrap/2.3.1/css/bootstrap-combined.min.css" rel="stylesheet">
				    <link href="//netdna.bootstrapcdn.com/twitter-bootstrap/2.3.1/css/bootstrap-responsive.min.css" rel="stylesheet">
				    <style>

				    /* GLOBAL STYLES
				    -------------------------------------------------- */
				    /* Padding below the footer and lighter body text */

				    body {
				      padding-bottom: 10px;
				      background-color: #5a5a5a;
				    }

				    /* CUSTOMIZE THE NAVBAR
				    -------------------------------------------------- */

				    /* Special class on .container surrounding .navbar, used for positioning it into place. */
				    .navbar-wrapper {
				      position: absolute;
				      top: 0;
				      left: 0;
				      right: 0;
				      z-index: 10;
				      margin-top: 20px;
				      margin-bottom: -90px; /* Negative margin to pull up carousel. 90px is roughly margins and height of navbar. */
				    }
				    .navbar-wrapper .navbar {

				    }

				    /* Remove border and change up box shadow for more contrast */
				    .navbar .navbar-inner {
				      border: 0;
				      -webkit-box-shadow: 0 2px 10px rgba(0,0,0,.25);
				         -moz-box-shadow: 0 2px 10px rgba(0,0,0,.25);
				              box-shadow: 0 2px 10px rgba(0,0,0,.25);
				      padding: 5px 10px 5px; 
				    }

				    /* Downsize the brand/project name a bit */
				    .navbar .brand {
				      font-size: 25px;
				      text-shadow: 0 -1px 0 rgba(0,0,0,.5);
				    }

				    /* Navbar links: increase padding for taller navbar */
				    .navbar .nav > li > a {

				    }

				    /* Offset the responsive button for proper vertical alignment */
				    .navbar .search-navbar {

				    }



				    /* CUSTOMIZE THE CAROUSEL
				    -------------------------------------------------- */

				    /* Carousel base class */
				    .carousel {
				      margin-bottom: 30px;
				      box-shadow: 3px 3px 3px 3px #000;
				    }

				    .carousel .container {
				      position: relative;
				      z-index: 9;
				    }

				    .carousel-control {
				      height: 80px;
				      margin-top: 0;
				      font-size: 120px;
				      text-shadow: 0 1px 1px rgba(0,0,0,.4);
				      background-color: transparent;
				      border: 0;
				      z-index: 10;
				    }

				    .carousel .item {
				      height: 500px;
				    }
				    .carousel img {
				      position: absolute;
				      top: 0;
				      left: 0;
				      min-width: 100%;
				      height: 500px;
				    }

				    .carousel-caption {
				      background-color: transparent;
				      position: static;
				      max-width: 550px;
				      padding: 0 20px;
				      margin-top: 200px;
				    }
				    .carousel-caption h1,
				    .carousel-caption .lead {
				      margin: 0;
				      line-height: 1.25;
				      color: #fff;
				      text-shadow: 0 1px 1px rgba(0,0,0,.4);
				    }
				    .carousel-caption .btn {
				      margin-top: 10px;
				    }



				    /* MARKETING CONTENT
				    -------------------------------------------------- */

				    /* Center align the text within the three columns below the carousel */
				    .marketing .span4 {
				      text-align: center;
				    }
				    .marketing h2 h3 {
				      font-weight: normal;
				    }
				    .marketing .span4 p {
				      margin-left: 10px;
				      margin-right: 10px;
				    }


				    /* Featurettes
				    ------------------------- */

				    .featurette-divider {
				      margin: 80px 0; /* Space out the Bootstrap <hr> more */
				    }
				    .featurette {
				      padding-top: 120px; /* Vertically center images part 1: add padding above and below text. */
				      overflow: hidden; /* Vertically center images part 2: clear their floats. */
				       box-shadow: 3px 3px 3px 3px #000;
				    }
				    .featurette-image {
				      margin-top: -120px; /* Vertically center images part 3: negative margin up the image the same amount of the padding to center it. */
				    }

				    /* Give some space on the sides of the floated elements so text doesn't run right into it. */
				    .featurette-image.pull-left {
				      margin-right: 40px;
				    }
				    .featurette-image.pull-right {
				      margin-left: 40px;
				    }

				    /* Thin out the marketing headings */
				    .featurette-heading {
				      font-size: 50px;
				      font-weight: 300;
				      line-height: 1;
				      letter-spacing: -1px;
				    }



				    /* RESPONSIVE CSS
				    -------------------------------------------------- */

				    @media (max-width: 979px) {

				      .carousel .item {
				        height: 350px;
				      }
				      .carousel img {
				        width: auto;
				        height: 350px;
				      }

				       .carousel .item {
				        height: 350px;
				      }
				      .carousel-caption {
				        width: 65%;
				        padding: 0 70px;
				        margin-top: 120px;
				      }
				      .carousel-caption h1 {
				        font-size: 30px;
				      }

				      .featurette {
				        height: auto;
				        padding: 0;
				      }
				      .featurette-image.pull-left,
				      .featurette-image.pull-right {
				        display: block;
				        float: none;
				        max-width: 40%;
				        margin: 0 auto 20px;
				      }
				    }


				    @media (max-width: 767px) {

				      .carousel {
				        margin-left: -20px;
				        margin-right: -20px;
				      }
				      .carousel .container {

				      }
				      .carousel .item {
				        height: 300px;
				      }
				      .carousel img {
				        height: 300px;
				      }
				      .carousel-caption {
				        width: 65%;
				        padding: 0 70px;
				        margin-top: 100px;
				      }
				      .carousel-caption h1 {
				        font-size: 30px;
				      }
				      .carousel-caption .lead,
				      .carousel-caption .btn {
				        font-size: 18px;
				      }

				      .marketing .span4 + .span4 {
				        margin-top: 40px;
				      }

				      .featurette-heading {
				        font-size: 30px;
				      }
				      .featurette .lead {
				        font-size: 18px;
				        line-height: 1.5;
				      }

				    }
				    </style>

				    <!-- Fav and touch icons -->
				    <link rel="apple-touch-icon-precomposed" sizes="144x144" href="/ico/apple-touch-icon-144-precomposed.png">
				    <link rel="apple-touch-icon-precomposed" sizes="114x114" href="/ico/apple-touch-icon-114-precomposed.png">
				      <link rel="apple-touch-icon-precomposed" sizes="72x72" href="/ico/apple-touch-icon-72-precomposed.png">
				                    <link rel="apple-touch-icon-precomposed" href="/ico/apple-touch-icon-57-precomposed.png">
				                                   <link rel="shortcut icon" href="/ico/favicon.png">
				  </head>
				  <body>
				  """

navbar = """
			    <!-- NAVBAR
			    ================================================== -->
			    <div class="navbar-wrapper">
			      <!-- Wrap the .navbar in .container to center it within the absolutely positioned parent. -->
			      <div class="container">
			        <div class="navbar navbar-inverse">
			          <div class="navbar-inner">
			            <a class="brand" href="#">What's Next?</a>
			            <div style="display: inline-block;" class="pull-right">
			              <form class="navbar-search">
			                <input type="text" class="search-query" placeholder="Search">
			              </form>
			            </div>
			          </div><!-- /.navbar-inner -->
			        </div><!-- /.navbar -->

			      </div> <!-- /.container -->
			    </div><!-- /.navbar-wrapper -->
		"""

footer = """



			    <!-- Le javascript
			    ================================================== -->
			    <!-- Placed at the end of the document so the pages load faster -->

			<script src="http://code.jquery.com/jquery-latest.js"></script>
			<script src="//netdna.bootstrapcdn.com/twitter-bootstrap/2.3.1/js/bootstrap.min.js"></script></script>

			<script type="text/javascript">
			     $('#myCarousel').carousel({interval: false})
			  </script>
			  </body>
			</html>
		"""

class HomePage(object):
	@cherrypy.expose
	def index(self):
		chosen = 2
		checkmark = """<img src="/static/img/checkmark.png" style="position: absolute; top: 7px; left: 7px;"/>"""
		carousel =  """
			    <!-- Carousel
			    ================================================== -->
			    <div id="myCarousel" class="carousel slide">
			      <div class="carousel-inner">
			        <div class="item active">
			          <img src="/static/img/albums/1.jpg" alt="">
			          <div class="container">
			            <div class="carousel-caption center">
			              <h1>Golden Slumbers</h1>
			              <p class="lead">Artist: The Beatles</p>
			              <p class="lead">Album: Abbey Road</p>
			            </div>
			          </div>
			        </div>
			        <div class="item">
			          <img src="/static/img/albums/2.jpg" alt="">
			          <div class="container">
			            <div class="carousel-caption">
			              <h1>El Schorcho</h1>
			              <p class="lead">Artist: Weezer</p>
			              <p class="lead">Album: Pinkerton</p>
			            </div>
			          </div>
			        </div>
			      </div>
			      <a class="right carousel-control" href="#myCarousel" data-slide="next">&rsaquo;</a>
			    </div><!-- /.carousel -->
			   	"""

		nextSongs = """
		    <!-- Marketing messaging and featurettes
		    ================================================== -->
		    <!-- Wrap the rest of the page in another container to center all the content. -->
		    <div class="container marketing">
		      <!-- Three columns of text below the carousel -->
		      <div class="row">
		        <div class="span4">
		          <div style="position: relative; left: 0; top: 0;">
		              <img class="img-polaroid" src="/static/img/albums/3.jpg" style="position: relative; top: 0; left: 0; filter: blur(5px) brightness(0.5);">
		    """
		if chosen==1:
			nextSongs+=checkmark
		nextSongs+="""</div>
	          <h3>Kanye West</h3>
	        </div><!-- /.span4 -->
	        <div class="span4">
	          <div style="position: relative; left: 0; top: 0;">
	              <img class="img-polaroid" src="/static/img/albums/4.jpg" style="position: relative; top: 0; left: 0; filter: blur(5px) brightness(0.5);">
	        """
		if chosen==2:
			nextSongs+=checkmark
		nextSongs+="""</div>
	          <h3>Justin Timberlake</h3>
	        </div><!-- /.span4 -->
	        <div class="span4">
	          <div style="position: relative; left: 0; top: 0;">
	              <img class="img-polaroid" src="/static/img/albums/5.jpg" style="position: relative; top: 0; left: 0;">
	              """
		if chosen==3:
			nextSongs+=checkmark
		nextSongs+="""</div>
	          </div>
	          <h3>Mumford & Sons</h3>
	        </div><!-- /.span4 -->
	      </div><!-- /.row -->

	      <footer>
	        <p>Taylor Seale & Iheanyi Ekechukwu 2013</p>
	      </footer>
	    </div><!-- /.container -->
		"""
		return header + navbar + carousel + nextSongs +  footer

		def 
conf = os.path.join(os.path.dirname(__file__), 'audite.config') 
cherrypy.quickstart(HomePage(),config=conf)