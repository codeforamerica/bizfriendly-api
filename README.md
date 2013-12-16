[![Build Status](https://travis-ci.org/codeforamerica/bizfriendly-api.png)](https://travis-ci.org/codeforamerica/bizfriendly-api)
[![Coverage Status](https://coveralls.io/repos/codeforamerica/bizfriendly-api/badge.png)](https://coveralls.io/r/codeforamerica/bizfriendly-api)

BizFriendly API
=========

BizFriendly teaches you how to use the internet to increase your quality of life, be more effecient at work, and perhaps even how to be a better citizen.

## <a name="about"></a>About
This is the API that powers the various BizFriendly applications.

## Made in Kansas City

<pre>

                     `..----..`                    
                 .-://////////:-.                 
               .:////////////////:.               
              -////////////////////-              
             -////////-....-////////-             
            `://////:`      `://////:`            
            .///////.        .///////.            
            `///////-       `:///////`            
  `-:::-.    -///////:`    `:///////-    .::::-`  
  ://////-    :///////:`  `:///////-    -//////:  
  :///////-    -///////: `:///////-    -///////:  
  `:///////:    -/////:`.:///////-    :///////:`  
   `:///////:`   .///:`.////////-   `:///////:`   
    `:///////:`   .::`.////////-   `:///////:`    
     `:///////:`   ``.////////-   `:///////:`     
      `:///////:.   .////////-   `:///////:`      
        -///////:. -////////-`. `:///////:`       
        `:////////:////////-`:/-:///////:`        
          :///////////////.`://////////:`         
           -/////////////.`://////////:           
            -///////////- ://////////:            
             -/////////-  `:////////-`            
              -///////.    .://////:              
               `.---.`      `.----.               
                                                  


       oyyyyyyyyyyy+          .yyyyyyyyyyyy       
       ``:yyyyyyy-``       ``` ```osyyyyyo:`      
          oyyyyyo`:/+ossyyyyyyyysso+////-+yy/`    
          oyyyyyo.yyyyyyyyyyyyyyyyyyyyyyo/+yyy/`  
          oyyyyyo.yyo+/:-..`.//////+oyyyyyyyyyyy/`
       .+-oyyyyyo`.       `/yyyyyy+`  .:oyyyyyyys:
     `oyy-oyyyyyo       `/yyyyyyo.       `:oyys:  
    :yyyy-oyyyyyo     `/yyyyyyo.            .-    
   /yyyyy-oyyyyyo   `/yyyyyyo.                    
  :yyyyy/ oyyyyyo `/yyyyyyo.                      
 `yyyyy+  oyyyyyo/yyyyyyy/                        
 /yyyyy`  oyyyyyyyyyyyyyyyo.                      
:yyyyys   oyyyyyyyyyoyyyyyyy/`                    
.yyyyy+   oyyyyyyy+. .oyyyyyys:                   
 /yyyys   oyyyyys`     -syyyyyyo.                 
 `syyyy:  oyyyyyo        /yyyyyyy+`               
  -yyyyy- oyyyyyo         `+yyyyyyy:              
   -yyyyy:.syyyyo           -syyyyyys.         ./-
    .syyyyo-/yyyo             :yyyyyyy+`     `/yy/
      /yyyyyo-:++              `+yyyyyyy:  `/yyyy:
       `/syyyys/.                .oyyyyyys-/ys+-.`
          -+syyyyyo/-.`           `:syyyyyy+-     
          o+:-:+syyyyyyyssooooossyyo./yyyyyyy/    
       ``.syyys+:--::/+oossssssoo+/:-`.syyyyyys-` 
       oyyyyyyyyyyy+                :yyyyyyyyyyyy/

</pre>

## <a name="demo"></a>Demo
Some example API calls:
	`http://app.bizfriend.ly/api/v1/categories`
	`http://app.bizfriend.ly/api/v1/lessons`
	`http://app.bizfriend.ly/api/v1/steps`

## <a name="development-setup"></a>Development Setup

BizFriendly is written in Python, and runs as a standalone [Flask application](http://flask.pocoo.org/).

1. For local development, uncomment the settings in setup.sh and set the correct values for your environment. 

2. Run a virtual environment and install all the requirements.
	`source setup.sh`

3. Run application.
    `python runserver.py`

4. Add content through the [Admin panel](http://127.0.0.1:5000/api/admin/categoryview/).

For continuous staging deployment:
set the Travis CI github hook for codeforamerica/bizfriendly-api on

## <a name="contributing"></a>Contributing
In the spirit of [free software][free-sw], **everyone** is encouraged to help
improve this project.

[free-sw]: http://www.fsf.org/licensing/essays/free-sw.html

Here are some ways *you* can contribute:

* by using alpha, beta, and prerelease versions
* by reporting bugs
* by suggesting new features
* by translating to a new language
* by writing or editing documentation
* by writing specifications
* by writing code (**no patch is too small**: fix typos, add comments, clean up
  inconsistent whitespace)
* by refactoring code
* by closing [issues][]
* by reviewing patches
* [financially][]

[issues]: https://github.com/codeforamerica/bizfriendly-api/issues
[financially]: https://secure.codeforamerica.org/page/contribute

## <a name="issues"></a>Submitting an Issue
We use the [GitHub issue tracker][issues] to track bugs and features. Before
submitting a bug report or feature request, check to make sure it hasn't
already been submitted. You can indicate support for an existing issue by
voting it up. When submitting a bug report, please include a [Gist][] that
includes a stack trace and any details that may be necessary to reproduce the
bug.

[gist]: https://gist.github.com/

## <a name="pulls"></a>Submitting a Pull Request
1. Fork the project.
2. Create a topic branch.
3. Implement your feature or bug fix.
4. Commit and push your changes.
5. Submit a pull request.

## <a name="copyright"></a>Copyright
Copyright (c) 2013 Code for America. See [LICENSE][] for details.

[license]: https://github.com/codeforamerica/bizfriendly-api

[![Code for America Tracker](http://stats.codeforamerica.org/codeforamerica/bizfriendly-api.png)](http://stats.codeforamerica.org/projects/bizfriendly-api)
