# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))
import sphinx_rtd_theme
import os
import sys 
#import importlib
#importlib.reload(sys)
reload(sys)
sys.setdefaultencoding('utf-8')

# -- Project information -----------------------------------------------------

project = 'OpenOCD和GDB简介与使用'
copyright = '2020, bouffalolab'
author = 'bouffalolab'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.imgmath',
    'sphinx_rtd_theme',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']
source_suffix = '.rst'

master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'zh'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_logo = 'content/logo.png'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_css_files = [
    'css/custom.css',
]

def setup(app):
    app.add_stylesheet("style.css")


latex_engine = 'xelatex'
latex_elements = {
    'fontenc': '\\usepackage{fontspec}',
    'fontpkg': '''\
\\usepackage[table,dvipsnames]{xcolor}
\\usepackage[utf8]{inputenc} 
\\usepackage[T1]{fontenc} 
\\usepackage{stix} 
\\usepackage[noindent,UTF8]{ctexcap}
\\usepackage[colorlinks,urlcolor=MidnightBlue,linkcolor=black]{hyperref}
\\setmainfont{Arial}
\\setCJKmainfont{SimSun}''',
    'geometry': '\\usepackage[a4paper,left=1.5cm, right=1.5cm,top=2cm,bottom=3.5cm]{geometry}',
    'preamble': '''\
\\usepackage[titles]{tocloft}
\\usepackage{xeCJK} 
\\usepackage{hyphenat}
\\usepackage{multirow}
\definecolor{tbcol}{RGB}{235,241,249}
\definecolor{regcell}{RGB}{196,214,236}

\\setlength{\\parskip}{8pt}   
\\linespread{1.4}

\\usepackage{LastPage}
\\usepackage{titletoc}
\\titlecontents{chapter}[3.5em]{ \zihao{5}\\vspace{-6pt} }{\contentslabel{1.3em}}{\hspace*{-2em}}{~\\titlerule*[0.8pc]{$.$}~\contentspage}

\\titlecontents{section}[6em]{ \zihao{5}\\vspace{-6pt} }{\contentslabel{2.8em}}{\hspace*{-2em}}{~\\titlerule*[0.8pc]{$.$}~\contentspage}

\\titlecontents{subsection}[9em]{\zihao{5}\\vspace{-6pt}}{\contentslabel{4em}}{\hspace*{-2em}}{~\\titlerule*[0.8pc]{$.$}~\contentspage}

\\usepackage{chngcntr}
\\counterwithin{figure}{chapter}
\\counterwithin{table}{chapter}

\\usepackage{titlesec}
\\usepackage{ctex}
\CTEXsetup[name={,}, number=\\arabic{chapter}]{chapter}

\\titlespacing*{\section}{0pt}{6pt}{0pt}
\\titleformat{\section}
{\\raggedright\zihao{4}\heiti\\bfseries\color{MidnightBlue}}
{\\thesection }
{6pt}
{}

\\titleformat{\subsection}
{\\raggedright\zihao{-4}\heiti\\bfseries\color{MidnightBlue}}
{\\thesubsection }
{6pt}
{}

\\titlespacing*{\subsection}{0pt}{6pt}{0pt}

\\newcommand\\bolddef[1]{\zihao{-4}\heiti\\bfseries #1}

%%%%%%%%%%liebiao%%%%%%%%%%%%%%
\\usepackage{indentfirst}
\\usepackage{enumitem}
\\setlist[itemize,1]{
leftmargin=15pt
} 

\\setlist[itemize,2]{
	leftmargin=20pt,
} 

\\setlist[enumerate,1]{
	leftmargin=15pt
} 

\\setlist[enumerate,2]{
	leftmargin=20pt,
} 

\\usepackage{fancyhdr}
\\pagestyle{fancy}
\\fancyhf{}
\\fancyhf{}
\\fancyfoot{}
\\fancyhead{}

\\renewcommand{\\footrule}{\color{MidnightBlue}\hrule width\\textwidth}
%\\renewcommand{\headrule}{\color{MidnightBlue}\hrule width\\textwidth}
\\renewcommand{\headrulewidth}{0pt}


\\fancyfoot[L]{\color{black} \\fontsize{9}{9} \selectfont OpenOCD和GDB简介与使用}
\\fancyfoot[C]{\color{black} \\fontsize{9}{9} \selectfont \\thepage / \pageref{LastPage}}
\\fancyfoot[R]{\color{black} \\fontsize{9}{9} \selectfont @2020 {\href{http://www.bouffalolab.com/}{\color{black} Bouffalo Lab}}}
%\cfoot{\\thepage}
\\fancypagestyle{plain}{
	\\fancyfoot[L]{\color{black} OpenOCD和GDB简介与使用}
	\\fancyhead{}
}

\\fancyhead[R]{\makebox[165pt][r]{\\fontsize{15}{15} \selectfont OpenOCD和GDB简介与使用}\\vspace{1pt}\hrule height 0pt \\vspace{10pt}}

%\\fancyhead[L]{\includegraphics[scale=0.3]{logo.png}}
\\fancyhead[L]{\makebox[50pt][l]{\includegraphics[scale=0.25]{logo.png}}\color{MidnightBlue}\hrule height 2pt \\vspace{0pt}  }

\\pagenumbering{arabic}
   
\\renewcommand\\arraystretch{1.3}
\\usepackage{colortbl}
\\newfloat{flowchart}{H}{loflow}
\\floatstyle{plaintop}
\\restylefloat{flowchart}
\\usepackage{float}

\\usepackage{caption}
\\newcommand\\smallpic[2]{
\\begin{figure}[H]
	\\hspace{73pt}
%	\\setlength{\\abovecaptionskip{0pt}}
%	\\setlength{\\belowcaptionskip{0pt}}
	\\captionsetup{
    justification=centering,
    singlelinecheck=false,
    margin={73pt,0pt}	
}
\\includegraphics{#2}
\\caption{#1}
%\\label{#3}
\\end{figure}
}

\\newcommand\\regover[1]
{
	\\begin{center}
		\\begin{longtable}[H]{|p{140pt}|p{350pt}|}
			\hline\hline
			\\rowcolor{tbcol}
			\\begin{minipage}{1.5cm}\\vspace{0.2cm}{\\bfseries 名称}\\vspace{0.2cm}\end{minipage}&\\bfseries 描述 \\\\
			
			\hline\hline
			\endhead
			\hline\hline
			\endlastfoot
			
			
		#1
		\end{longtable}					  							
	\end{center}	
}

\\usepackage{hhline}

\\newcommand\\regbit[1]
{
	\\begin{table}[H]
	    \\footnotesize
		\\begin{tabular}[c]{|p{19.7pt}<{\centering}|p{19.7pt}<{\centering}|p{19.7pt}<{\centering}|p{19.7pt}<{\centering}|p{19.7pt}<{\centering}|p{19.7pt}<{\centering}|p{19.7pt}<{\centering}|p{19.7pt}<{\centering}|p{19.7pt}<{\centering}|p{19.7pt}<{\centering}|p{19.7pt}<{\centering}|p{19.7pt}<{\centering}|p{19.7pt}<{\centering}|p{19.7pt}<{\centering}|p{19.7pt}<{\centering}|p{19.7pt}<{\centering}|}
			\hline
			\\rowcolor{tbcol}
			
			
			#1
		\end{tabular}					  							
	\end{table}			
}

\\newcommand\\regdes[1]
{
	\\begin{center}
		\small
		
		\\begin{longtable}[c]{|p{30pt}<{\centering}|p{128pt}<{\centering}|p{20pt}<{\centering}|p{40pt}<{\centering}|p{233pt}|}
			\hline\hline
			\\rowcolor{tbcol}
			\\begin{minipage}{1.5cm}\\vspace{0.2cm}{\\bfseries \centering 位}\\vspace{0.2cm}\end{minipage}&\\bfseries 名称&\\bfseries 权限 &\\bfseries 复位值&{\\bfseries \centering 描述} \\\\
			
			\hhline{|=====|}
			\endhead
			\hline
			\endlastfoot
			
			
			#1
			
		\end{longtable}					  							
	\end{center}	
	\\vspace{-0.6cm}
}

% 目录
\\usepackage{shorttoc}


\\usepackage{graphicx}
\\hyphenpenalty=5
\\tolerance=1
\\usepackage{ragged2e}


\\usepackage{array}
\\newcommand{\\tabincell}[2]{\\begin{tabular}{@{}#1@{}}#2\end{tabular}}  %表格自动换行
\\cftsetpnumwidth{1.0cm}\\cftsetrmarg{1.2cm}
\\setlength{\\cftchapnumwidth}{0.75cm}
\\setlength{\\cftsubsecnumwidth}{1.5cm}
\\setlength{\\cftsecindent}{\\cftchapnumwidth}
\\setlength{\\cftsecnumwidth}{1cm}''',
    'fncychap': '\\usepackage[Bjornstrup]{fncychap}',
    'printindex': '\\footnotesize\\raggedright\\printindex',
}
#latex_show_urls = 'footnote'