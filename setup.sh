mkdir -p ~/.streamlit/

echo "\
[server] \n\
ports=$PORT\n\
enableCORS=false\n\n
headless=true\n\
\n\
" > ~/.streamlit/config.toml