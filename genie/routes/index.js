
const app = require('../app');

// Router setup.
app.use('/', require('./root'));
app.use('/countries',require('./country'));
app.use('/diseases',require('./disease'));
app.use('/gene_pmid_titles',require('./gene_pmid_title'));
app.use('/gene_scores',require('./gene_score'));
app.use('/job_insert',require('./job_insert'));
app.use('/key2ids',require('./key2id'));
app.use('/id2keys',require('./id2key'));
app.use('/pmid_abstracts',require('./pmid_abstract'));
app.use('/pmid_counts',require('./pmid_count'));
app.use('/gene_pmid_counts',require('./gene_pmid_count'));
app.use('/hgnc2symbols',require('./hgnc2symbol'));
app.use('/downloader',require('./downloader'));
