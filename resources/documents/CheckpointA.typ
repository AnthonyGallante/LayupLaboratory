#import "./src/apa7ish.typ": *

#show: conf.with(
  title: "An Intriguing Title",
  subtitle: "A causal inference approach to March Madness",
  documenttype: "Term Project",
  authors: ((name: "Anthony Gallante", affiliation: "Northwestern University\nSchool of Professional Studies"),),
  abstract: [ // The abstract serves as an executive summary of the proposed research. 

    // Identify the industry sector or selected firms 
    // Identify the financial asset or portfolio of assets associated with the sector or firms 
    // Briefly describe the overall goal of the term project: 
    // Developing a network model of firms 
    // Developing a causal forecasting model for the selected asset(s) 

    #lorem(120)
    ],
  date: "February 2, 2026",
)

// To cite a paper: @gilani_2021_hoopR

= Introduction // The introduction explains motivation and context for the research. 
// Describe why you are conducting this research 
// Identify the management or decision-making problem of interest 
// Identify the likely users of the research results and their high-level questions 


= Literature Review // The literature review situates your project within existing work. 
// Identify prior research related to your industry sector, network modeling approach, or causal analysis 
// Summarize how others have approached similar problems 


= Methods // The methods section outlines how you plan to conduct the research. 
// Describe your initial thoughts about the data 
// Identify likely node types and link types for your planned network model 
// Describe the network science and/or probabilistic graphical modeling methods you expect to use 


= Results // At this early stage, this section should focus on expected outcomes rather than finalized findings.
// Identify the data sources you plan to use 
// Describe how these data will serve as inputs to the network and causal models models 
// Explain what you expect to learn from the analysis 


= Conclusions // The conclusions section reflects on the anticipated value and limitations of the research. 
// Summarize what you expect the research to reveal 
// Discuss any concerns about the topic, data availability, or planned methods 
// Explain how the results are expected to be useful in addressing the identified management problem 
// Briefly describe how results may ultimately be communicated to users (e.g., reports, visualizations, dashboards) 


#bibliography("references.bib", style: "chicago-notes")
// Or for author-date:
// #bibliography("refs.bib", style: "chicago-author-date")