---
layout: post-index
---
<ul>
  {% for post in site.posts %}
    <li>
      <h2><a href="{{site.BASE_PATH}}{{ post.url }}">{{ post.title }}</a></h2>
      <div class="ficha-metadata">
          <span class="metadata-input">{{ post.date | date_to_string }}</span>        
      </div>
    </li>
  {% endfor %}
</ul>