.. include:: /features/deep-sidebar.rst

#############
 SQL Alchemy
#############

Database Scalability:

- Automatically batches and minimizes the number of inserts sent to the database
- Loads just the data you want: supports both eager loading and lazily loading of objects
- Objects can map to any relation, not just a physical table
- Multi-database support
- High quality legacy database support

Template engine:

- Supports Genshi, Mako and Jinja out of the box
- All template engines support template functions or macros
- All template engines have support for python expressions (no need to learn a whole new language for your templates)
- Genshi supports match tags that allow you to easily create your own template tag libraries
- Genshi helps to ensure valid parsible HTML output
- Genshi supports XML output natively -- not via string concatenation so output is always valid
- Genshi supports intelegent (context aware) automatic escaping which reduces the risk of cross site scripting vulnerabilities in your app

Caching:

- High performace cache, that automatically protects you from the dogpile effect.
- Support for multiple back-ends include dbm, file, memory, cookie, memcached, and database
- Signed cookie's to prevent session hijacking/spoofing
- Cache's can be divided into namespaces
- You can pass in a function to automatically create new cache copies after expiration

JavaScript and Ajax:
