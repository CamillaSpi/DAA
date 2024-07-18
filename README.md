# DNA Contamination 
## Overview
Often the various laboratory processes used to isolate, purify, clone, copy, maintain, probe, or sequence a DNA string will cause unwanted DNA to become inserted into the string of interest or mixed together with a collection of strings. Contamination of protein in the laboratory can also be a serious problem. During cloning, contamination is often caused by a fragment (substring) of a vector (DNA string) used to incorporate the desired DNA in a host organism, or the contamination is from the DNA of the host itself (for example bacteria or yeast). Contamination can also come from very small amounts of undesired foreign DNA that gets physically mixed into the desired DNA and then amplified by PCR (the polymerase chain reaction) used to make copies of the desired DNA.
Contamination is an extremely serious problem, and there have been embarrassing occurrences of large-scale DNA sequencing efforts where the use of highly contaminated clone libraries resulted in a huge amount of wasted sequencing. These embarrassments might have been avoided if the sequences were examined early for signs of likely contaminants, before large-scale analysis was performed or results published.
Indeed, often, the DNA sequences from many of the possible contaminants are known. These include cloning vectors, PCR primers, the complete genomic sequence of the host organism (yeast, for example), and other DNA sources being worked with in the laboratory.
## Developed System
The goal of the implemented system is to make sure that given an isolated DNA sequence and a set of possible contaminants, the level of contamination of each contaminant within the string can be known. This level corresponds to the number of maximal substrings of the contaminant found within the DNA sequence. 
Specifically, it was implemented a class **DNAContamination** that allows to verify the degree of contamination in a DNA sequence by a set of contaminants C. 
The main methods implemented in the class are:
- `DNAContamination(s, l)` builds a DNAContamination object; it takes in input the contaminant s and the contamination threshold l (the contaminant set C is initially empty);
- `addContaminant(c)` adds contaminant c to the set C and saves the degree of contamination of s by c, it shuld run in in time O(((len(s)+len(c))^2) + log m), where m is the number of total contaminants that would be added;
- `getContaminants(k)` returns the k contaminants with larger degree of contamination among the added contaminants, it should run in time O(k log m).

It was also implemented the function `test(s,k,l)` that starting from some DNA strings, returns the indices of the k contaminants in the dataset with larger degree of contamination in the DNA sequence, assuming l as contamination threshold, in increasing order. 
It was necessary for the proposed solution to be very fast and efficient.
The proposed solution involved the use of a **Suffix Tree**, for more details about the implemented functions refer to `DNAContamination`.

# Social Network Sentiment Analysis 
## Overview
A very famous Social Network is designing a tool for forecasting the results of US presidential elections. This tool assumes that the vote of voter v is influenced by the relationships between v and other nodes in the network: if v has many friends voting for Democrats or many enemies voting for Republicans, then it is more likely that v votes for Democrats. Starting from these assumptions it was neccesary to develop two different types this tool.
- First Tool Version: The amount of data owned by the Social Network allows for powerful sentiment analysis that provides a very precise estimate of the level of enmity evw ≥ 0 for each pair of voters v and w that are friends on this social network. The Social Network's tool groups voters for Democrats and Republicans so that the level of enmity within each group is low, and the level of enmity among the two groups is as large as possible. Hence, the level of enmity in a set of voters is computed as the sum of enmities among each pair of these voters that are friends on the Social Network.
- Second Tool Version: At some times, the Social Network decided to change the sentiment analysis algorithm, and to
compute the level of friendship fvw ≥ 0 for each pair of voters v and w that are friends on this social network. Note that levels of friendship and enmity are unrelated. To this reason, the Social Network needs to adapt its tool for forecasting the results of US Presidential elections. So the tool now needs to group voters for Democrats and Republicans so that the level of friendship within each group is large, and the level of friendship among the two groups is as low as possible. (As for enmity, the level of friendship in a set of voters is computed as the sum of friendships among each pair of these voters that are friends on the social network).
Moreover, the Social Network developed a new sentiment analysis algorithm that assigns to each node v the likelihood dv that v votes for Democrats and the likelihood rv that v votes for Republicans. The improved tool hence requires also to maximize
the total likelihood of returned groups, where the total likelihood is the sum over all voters v of the likelihood that v votes for the candidate of the group at which it is assigned.

## Developed System
- First Tool Version: it has been implemented a `facebook_enmy(V, E)` function that takes in input:
    - a Python set V of voters, and
    - a Python dictionary E whose keys are Python tuples representing pairs of voters that have a friendship relationship on Facebook, and whose values represent the enmity level that  Facebook assigned to the corresponding pair, and returns two Python sets, D and R, corresponding to voters for Democrats and
Republicans, respectively.

    After creating an undirected graph in an appropriate way to solve the problem, the idea is to sort vertices according to their weights, to choose the major and establish in which set it is convenient to insert it in order to maximize the enmity between the two groups. This fucntion is implemented using **dynamic programming** with the purpose of getting out of the local maximums to reach the absolute maximums, collecting a series of solutions, sometimes even worse ones, to then choose the best one at the end.

- Second Tool Version: it has been implemented a `facebook_friend(V, E)` that takes in input:
    - a Python dictionary V whose keys represent voters, and values are Python tuples with the first entry being the likelihood for Democrats and the second being the likelihood for Republicans;
    - a Python dictionary E whose keys represent pairs of voters that have a friendness relationship on Facebook, and whose values represent the friendship level that Facebook assigned to the corresponding pair, and returns two Python sets, D and R, corresponding to voters for Democrats and Republicans, respectively.

    The idea of the **max-flow (min-cut) algorithm** is applied to create a division into the two sets in order to minimize the level of friendship among the two groups, to maximize that within each group and to maximize the total likelihood of the returned groups (given by the sum over all voters v of the likelihood that v votes for the candidate of the group at which it is assigned). After creating a network flow suitably to solve the problem, while there is a path from the source to the destination, the value of forward edges is decreased considering the bottleneck of the path found and the value of backword edges is increased considering the bottleneck of the path found. When there are no more paths from source to destination the two sets are created considering that the voters reachable from the super Source must stay in the same set of super source (Democrats) and the other in the same set of super target (Republicans).

For more details about the implemented functions refer to `SocialNetworkSentimentAnalysis`.

#Feedback
For any feedback, questions or inquiries, please contact the project maintainers listed in the Contributors section.

