def get_stats(al, fname, fp_csv):
    m,mx,mn,sd = [],[],[],[]
    for a in al:
        m.append(round(np.mean(a),2))
        sd.append(round(np.std(a),2))
        mn.append(round(np.min(a),2))
        mx.append(round(np.max(a),2))
    df = pd.DataFrame(np.column_stack([fname, m, mn, mx, sd]), columns=['fname','mean', 'min','max',' std'])
    df.to_csv(fp_csv)


def contour_range(start,stop, incr):
    # contours for formatting
    l = list(range(start, stop, incr))
    l = [str(v) for v in l]
    l  = ' '.join(l)
    return(l)
