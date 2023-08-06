Fellow linguists: A compendium
==============================

.. meta::
    :description lang=en:
        ...



Web corpora as scientific objects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Web corpora are first and foremost archives and as such they be seen as a library. It is a bit like browsing automatically a library of hyperlinks. What we need are robots managing collections, similar to librarians going to particular portions of the web to fetch documents we are interested in and then gathering them on our designated shelf, so that we can later find them.

And it's also about making data collection manageable in the term of the of an oversight that you get over what you just retrieve. So the books that landed on your shelf. 

And secondly, it's about making things observable. And in that respect. It can also be compared to a telescope or a microscope in the way that through the lenses. 

And through the scientific apparatus, you get access to a scientific reality or to a particular part of the world or of space that you wouldn't get. To observe otherwise.


Seen from a practical perspective, the purpose of focused web corpora is to complement existing collections, as they allow for better coverage of specific written text types and genres, especially the language evolution seen through the lens of user-generated content, which gives access to a number of variants, socio- and idiolects. the case of blogs (Barbaresi 2019)



Googleology is bad science (Kilgarriff 2007)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


- The commercial search engines do not lemmatise or part-of-speech tag
- The search syntax is limited
- There are constraints on numbers of queries and numbers of hits per query
- Search hits are for pages, not for instances
- Search engine counts are arbitrary
- The hits are sorted according to a complex and unknown algorithm


    “An alternative is to work like the search engines, downloading and indexing substantial
    proportions of the web, but to do so transparently, giving reliable figures, and supporting
    language researchers’ queries.” (Kilgarriff 2007)
	

Steps
~~~~~


    “The process involves crawling, downloading, ’cleaning’ and de-duplicating the data, 
    then linguistically annotating it and loading it into a corpus query tool.” (Kilgarriff 2007)


1. Crawling, downloading, cleaning and de-duplicating the data: motivation of this software package
2. Annotation sometimes conflated with corpus tools


+ Accesses to it

    “One reason for blurring the separation between the data and tools of corpus linguistics is that the data itself can vary tremendously in quality and quantity depending on the research design. [...]
    Another reason is that the tools used in corpus linguistics are software based, and thus, abstract in nature.” (Anthony 2013)


Post hoc evaluation
~~~~~~~~~~~~~~~~~~~

It relies on the assumption that “the Web is a space in which resources are identified by Uniform Resource Identifiers (URIs).” (Berners-Lee et al., 2006)


The Web is however changing faster than the researchers’ ability to observe it (Hendler et al., 2008), and a constant problem faced by web resources resides in meta-information and categorization.


The actual contents of a web corpus can only be listed with certainty once the corpus is complete. In fact, corresponding to the potential lack of information concerning the metadata of the texts is a lack of information regarding the content, whose adequacy, focus and quality has to be assessed in a post hoc evaluation (Baroni et al., 2009).




Corpus types and resulting methods
----------------------------------

- General-purpose vs. ad hoc web corpora (Barbaresi 2015)
- Also known as “Miniweb” vs. Domain specific corpora in the `WebCorp LSE <https://wse1.webcorp.org.uk/home/corpora.html>`_ typology.
- General vs. specialized (Gries & Newman 2014)


1. Tailor-made corpus targeting already known sources (focused crawling)
   → Anwendung von Kriterien, um das Suchfeld einzuschränken (Webstruktur/Domains oder Inhalt/Themen)


2. “Open-end” approach & automated web browsing (web crawling, broad crawls)
   → braucht „Seeds“, hüpft von Seite zu Seite

3. Use of search engines (focused searches, BootCaT method)



General-purpose corpora
~~~~~~~~~~~~~~~~~~~~~~~

On the one hand, there are general purpose corpora, which are supposed to encompass a large amount of texts and a gamut of text types and text genres. Their significance arises from it, which can make them representative in some way. Corpus designers usually rely on the fact that potential small irregularities are going to be smoothed out by the sheer number of texts, so that empirical findings in the corpus are expected to be statistically relevant all the same.

Maybe representative of a genre or of a particular source, in the case of web corpus, like a Mini web, because the Web is too large to be completely retrieved and stored in a database.

See the Tanguy 20??

And so the goal for linguists to get a statistical perspective on norms.
(It's also a general aspect of norms as a See the articles by Habert.)


These corpora are often found at dedicated research institutions, as the building and maintenance is costly in time and resources. In the case of web corpora, this involves first an extensive web crawling phase, using mostly breadth-first techniques. Second, the text pre-processed. Meaning that a selection of resources of the documents or relevant extracts. Finally, loaded into corpus tool, which in that case, mostly involves tailored database applications.

(not covered here)


Specialized corpora
~~~~~~~~~~~~~~~~~~~


On the second hand, there are specialized corpora which focus on a particular genre or or a particular source. They can be opportunistic in nature but they mostly involve prior knowledge of the contents and also a certain amount of control over what comes into the corpus.
Contrarily to open ended-corpora, the goal for linguists is to get a better coverage of particular linguistic settings or phenomena.


Corpus building comprises three phases.
First, the texts are discovered and listed. Then they are downloaded, possibly using web crawling techniques which are not as extensive as in the other case since it is mainly about fetching and processing. 
Then a processed version is stored, which is in itself the linguistic corpus. It can be indexed by a corpus-query tool or be made available using standardized formats used by the research Community such as XML or XML TEI.

    “manually selecting, crawling and cleaning particular web sites with large and good-enough-quality textual content” (Spoustová & Spousta, 2012)


See tutorial0.html



Corpus types and resulting methods
----------------------------------


Boilerplate removal
~~~~~~~~~~~~~~~~~~~

(will hopefully be addressed in a blog post soon)




Selection of sources
~~~~~~~~~~~~~~~~~~~~


A different series of question arise when randomly searching for text on the Internet: Is what is a text? When does it stop to be a text? What should be included in the corpus?
Sometimes there are scraps of text coming from processing boilerplate removal face for instance, or simply because certain texts types like classified ads. It takes it or that we are interested in or is it something we don't want?


see the challenges described in Schäfer et al. 2013




Practical guidelines
--------------------

works best with pages centered on a main text, e.g. blog & news articles, or simply pages without boilerplate.



web pages only, main text extracted, metadata, and comments.
all with a reasonable accuracy although it is not perfect.

Where can we find URLs? → sources.html

Tutorial: Gathering a custom web corpus tutorial0.html

Curating a list of sources (on site- or page-level), involves URL management of some sort. → courlan
see url-management.html



Caveats
~~~~~~~


Now, moving on to the problems related to data collection. 


Platforms/social networks

Forums



You have a number of platforms and social networks. That second be growth or whose data can be used 3D without the agreement of the company behind the network. Then you have news article disappearing behind pay walls for instance. 

And you also have text, that can be reached because of link rot. Are because something wrong happens. The techniques that I used. For instance, documents without metadata can sometimes not be properly identified and classified. So it's like a lost book in a library. 

And then you have a number of technical problems related to the web servers that you need to. 

Get in contact with, in order to retrieve the data. See the page on the downloads. And you have a number of problems that can arise on your machine because you made get out of RAM.


Are have problems with your internet connection of bandwidth? Or simply run out of space to store the data or two out of capacity to process it. That's on that only applies to really larger endeavors. For specialized compass. Up to tens of thousands of documents even on an old computer software should work fine. 




Corpus analysis and querying software
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Output formats: TXT, XML and XML-TEI quite frequent in corpus linguistics.



- `Antconc <https://www.laurenceanthony.net/software/antconc/>`_ is expected to work with TXT files
- `CorpusExplorer <https://notes.jan-oliver-ruediger.de/software/corpusexplorer-overview/>`_ supports CSV, TXT and various XML formats
- `Corpus Workbench (CWB) <https://cwb.sourceforge.io/>`_ uses verticalized texts whose origin can be in TXT or XML format
- `LancsBox <http://corpora.lancs.ac.uk/lancsbox/>`_ support various formats, notably TXT & XML
- `TXM <http://textometrie.ens-lyon.fr/?lang=en>`_ can take TXT, XML & XML-TEI files as input
- `Voyant <https://voyant-tools.org/>`_ support various formats, notably TXT, XML & XML-TEI
- `Wmatrix <http://ucrel.lancs.ac.uk/wmatrix/>`_ can work with TXT and XML
- `WordSmith <https://lexically.net/wordsmith/index.html>` supports TXT and XML

Further corpus analysis software can be found on `corpus-analysis.com <https://corpus-analysis.com/>`_.

`Data science tools <tutorial-data.html>`_




References
----------


- Anthony, L. (2013). A critical look at software tools in corpus linguistics. Linguistic Research, 30(2), 141-161.
- Barbaresi, A. (2015). Ad hoc and general-purpose corpus construction from web sources (Doctoral dissertation, ENS Lyon).
- Barbaresi, A. (2019). The Vast and the Focused: On the need for thematic web and blog corpora. In 7th Workshop on Challenges in the Management of Large Corpora (CMLC-7) (pp. 29-32). Leibniz-Institut für Deutsche Sprache.
- Baroni, M., & Bernardini, S. (2004). BootCaT: Bootstrapping Corpora and Terms from the Web. In Proceedings of LREC 2004 (pp. 1313-1316).
- Baroni, M., Bernardini, S., Ferraresi, A., & Zanchetta, E. (2009). The WaCky wide web: a collection of very large linguistically processed web-crawled corpora. Language resources and evaluation, 43(3), 209-226.
- Gries, S. T., & Newman, J. (2014). Creating and using corpora. In Research methods in linguistics, Podesva, R.J., & Sharma, D. (eds.), 257-287.
- Kilgarriff, A. (2007). Googleology is bad science. Computational linguistics, 33(1), 147-151.
- Schäfer, R., Barbaresi, A., & Bildhauer, F. (2013). The Good, the Bad, and the Hazy: Design Decisions in Web Corpus Construction. In 8th Web as Corpus Workshop, pp.7-15, ACL SIGWAC.
- Spoustová, J., & Spousta, M. (2012). A High-Quality Web Corpus of Czech. In Proceedings of the Eighth International Conference on Language Resources and Evaluation (LREC'12) (pp. 311-315).


