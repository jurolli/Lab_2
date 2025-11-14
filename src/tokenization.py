
def tokenization(st):
    while '  ' in st:
        st = st.replace('  ', ' ')
    
    st = st.split()
    i = 0
    while i < len(st):
        if st[i][0] == '"':
            while st[i][-1] != '"':
                st[i] = ' '.join([st[i], st[i + 1]])
                st.pop(i + 1)
        if st[i][0] == '"' and st[i][-1] == '"':
            st[i] = st[i][1:-1]
        i += 1
    return st