export default {
  common: {
    title: 'GENAX',
    githubLink: 'https://github.com/arbc139/Capstone-2017-2',
    documentLink: 'https://help.genax.tools/',
    nextButton: 'Next',
    downloadButton: 'Download',
    linkMessage: 'click here',
  },
  mainTabs: {
    about: {
      label: 'About',
    },
    run: {
      label: 'Run',
    },
    performance: {
      label: 'Performance',
    },
  },
  stepper: {
    query: {
      errorMessage: 'Query is empty',
    },
    period: {
      errorMessage: 'Period is not selected',
    },
    parameter: {
      errorMessage: 'Incorrect parameter',
    },
    selectNodeSize: {
      errorMessage: 'Incorrect node size',
    },
    submit: {
      errorMessage: 'Disable to create job',
    },
    pmidCount: {
      errorMessage: "It's over 500000. please adjust query or period.",
    },
  },
  query: {
    title: 'Query page',
    placeholder: 'Please enter a SQL statement.',
    condition: {
      input: {
        placeholder: 'Please enter a keyword.',
      },
    },
    help: {
      title: 'Welcome to GENAX',
      instructions: [
        { id: 0, content: 'For given keywords, GENAX will find out which genes are related to them.' },
        { id: 1, content: 'You can add or remove keywords by pressing the button.' },
        { id: 2, content: 'You can also take advantage of the advance search feature of PubMed.' },
        {
          id: 4,
          content: 'To learn more about keyword building, ',
          link: 'https://help.genax.tools/keyword.html',
        },
      ],
    },
  },
  period: {
    title: 'Period page',
    units: {
      all: 'All',
      lastOneYear: 'Last 1 year',
      lastThreeYears: 'Last 3 years',
      lastFiveYears: 'Last 5 years',
      lastTenYears: 'Last 10 years',
      custom: 'Custom',
    },
    help: {
      title: 'Please Choose the Time Period',
      instructions: [
        { id: 0, content: 'According to the period of time you choose, GENAX will dynamically generate the results.' },
        {
          id: 1,
          content: 'To learn more about time period, ',
          link: 'https://help.genax.tools/time-period.html',
        },
      ],
    },
  },
  parameter: {
    title: 'Parameter page',
    labels: {
      MIN_SUP: 'Minimum Support of an Edge',
      MAX_PVAL: 'Maximum P-value of an Edge',
      COOC_EM: 'The Metric which to Make Edge',
    },
    selects: {
      COOC_EM: {
        support: 'Support',
        logPvalue: 'Log(P-value, 10)',
        oddRatio: 'Odd Ratio',
        relativeRisk: 'Relative Risk',
        lift: 'Lift',
        chiSquaredStatistic: 'Chi-Squared Statistic',
        phiCoefficient: 'Phi Coefficient',
        contingencyCoefficient: 'Contingency Coefficient',
      },
    },
    errorMessages: {
      MIN_SUP: 'Please input 0.00001 ~ 1 floating point value.',
      MAX_PVAL: 'Please input 0.000001 ~ 1 floating point value.',
      COOC_EM: 'Please select right field.',
    },
    help: {
      title: 'Please Set Co-occurrence Mining Options.',
      instructions: [
        { id: 0, content: 'GENAX uses co-occurrence mining to construct networks between genes.' },
        { id: 1, content: 'The options on the left are the conditions necessary to run the GENAX algorithm.' },
        { id: 2, content: 'Default options are provided.' },
        {
          id: 3,
          content: 'To learn more about co-occurrence mining options, ',
          link: 'https://help.genax.tools/co-occurrence-mining-options.html',
        },
      ],
    },
  },
  selectNodeSize: {
    title: 'Select node size page',
    nodeSize: {
      label: 'Node Size',
      errorMessage: 'Please select node size range in 1 ~ 100',
    },
    metricScore: {
      label: 'Minimum Support of Single Occurring Node',
      errorMessage: 'Please select metric score range in 0.000001 ~ 1',
    },
    help: {
      title: 'Please Set Single Occurring Node Options.',
      instructions: [
        { id: 0, content: 'GENAX forms a network of genes that appear simultaneously in the paper.' },
        { id: 1, content: 'In the case of a gene that appears alone in the papers as a single occurring node, they will receive a higher score when calculating Katz centrality.' },
        {
          id: 2,
          content: 'To learn more about single occurring node, ',
          link: 'https://help.genax.tools/single-occurring-node.html',
        },
      ],
    },
  },
  email: {
    title: 'Email page',
    input: {
      placeholder: 'Please enter the email. (Optional)',
    },
    help: {
      title: 'Please Enter Your E-mail (optional).',
      instructions: [
        { id: 0, content: 'GENAX will send you an e-mail when the job starts and ends.' },
        { id: 1, content: 'If you do not enter an email address, you will not be notified about the start and end of the task.' },
        {
          id: 2,
          content: 'To learn more about e-mail notification, ',
          link: 'https://help.genax.tools/job-notification.html',
        },
      ],
    },
  },
  checkParameter: {
    labels: {
      query: 'Query',
      period: 'Period',
      parameters: {
        MIN_SUP: 'Minimum support of an edge',
        MAX_PVAL: 'Maximum p-value of an edge',
        COOC_EM: 'The metric by which to make edge',
      },
      metricScore: 'Minimum support of a single occurring node',
      nodeSize: 'Node size',
      email: 'Email',
      pmidCount: 'Expected pmid counts',
    },
  },
  result: {
    status: {
      type: {
        yet: 'Not yet',
        running: 'Running',
        done: 'Done',
      },
      paper: 'Paper Collect',
      networkConstruction: 'Network Build',
      networkAnalysis: 'Network Analysis',
    },
    table: {
      methodType: {
        association: 'Association',
        associationSingle: 'Association (Single node)',
        coOccurence: 'Co-occurrence',
        coOccurenceSingle: 'Co-occurrence (Single node)',
      },
      download: {
        associationEdge: 'Association network edge',
        coOccurenceEdge: 'Co-occurrence network edge',
        singleOccuringNode: 'Single occuring node',
        geneScoresByAssociation: 'Gene scores by association',
        geneScoresByAssociationNode: 'Gene scores by association + node',
        geneScoresByCoOccurence: 'Gene scores by co-occurrence',
        geneScoresByCoOccurenceNode: 'Gene scores by co-occurrence + node',
      },
    },
    instruction: {
      essay: 'Number of Papers',
      construction: {
        associationEdge: 'Number of Association Edges',
        coOccurenceEdge: 'Number of Co-occurrence Edges',
        singleOccuringNode: 'Number of Single Occuring Nodes',
      },
      analysis: {
        associationGene: 'Number of Genes (Association)',
        associationNodeTotal: 'Number of Genes (Association & Single Occurring Nodes)',
        coOccurenceGene: 'Number of Genes (Co-occurrence)',
        coOccurenceNodeTotal: 'Number of Genes (Co-occurrence & Single Occurring Nodes)',
      },
    },
    reference: {
      title: 'References of gene {symbol} of the query',
    },
    parameter: {
      searchOptions: {
        labels: {
          searchQuery: 'Search Query',
          searchPeriod: 'Search Period',
          metricScore: 'Minimum support of a single occurring node',
          singleOccuringNodeSize: 'Single Occuring Node Size',
          userEmail: 'User Email',
        },
      },
      coOccurenceOptions: {
        labels: {
          MIN_SUP: 'Minimum support of an edge',
          MAX_PVAL: 'Maximum p-value of an edge',
          COOC_EM: 'The metric by which to make edge',
        },
        selects: {
          COOC_EM: {
            support: 'Support',
            logPvalue: 'Log(P-value, 10)',
            oddRatio: 'Odd Ratio',
            relativeRisk: 'Relative Risk',
            lift: 'Lift',
            chiSquaredStatistic: 'Chi-Squared Statistic',
            phiCoefficient: 'Phi Coefficient',
            contingencyCoefficient: 'Contingency Coefficient',
          },
        },
      },
    },
    time: {
      notDone: 'Running...',
      dateFormat: 'Job started at {startDisplayDate} and ended at {endDisplayDate}',
      durationFormat: 'It took {displayHour} hours {displayMin} min {displaySec} sec to finish.',
    },
  },
};
