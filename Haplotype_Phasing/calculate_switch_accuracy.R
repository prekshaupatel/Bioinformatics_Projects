# Calculate switch error rates.

get_switch_error = function(haplotypes_output_file, haplotypes_test_file, random=T){
  
  haplotypes_output = read.table(haplotypes_output_file, header=F)
  haplotypes_test = read.table(haplotypes_test_file,header=F)
  het_sites = haplotypes_test[,1] + haplotypes_test[,2] ==1
  haplotypes_output_hets = haplotypes_output
  haplotypes_test_hets = haplotypes_test
  switch_errors = c()
  for(i in seq(1,ncol(haplotypes_output),by=2)){
    het_sites = haplotypes_test[,i] + haplotypes_test[,(i+1)] ==1
    align = haplotypes_test_hets[1,i] == haplotypes_output_hets[1,i]
    haplotypes_output_hets = haplotypes_output[het_sites,]
    haplotypes_test_hets = haplotypes_test[het_sites,]
    if(align){
      h1_test = haplotypes_test_hets[,i]
      h2_test = haplotypes_output_hets[,i]
    }else{
      h1_test = haplotypes_test_hets[,i]
      h2_test = haplotypes_output_hets[,i+1]
    }
    h1_test[h1_test==0] = -1
    h2_test[h2_test==0] = -1 
    switches_test = h1_test[1:(length(h1_test)-1)] * h1_test[2:(length(h1_test))]
    switches_output = h2_test[1:(length(h2_test)-1)] * h2_test[2:(length(h2_test))]
    switch_error = sum(switches_test * switches_output == -1)/ length(switches_test)
    switch_errors = c(switch_errors, switch_error)
  }
  switch_error= mean(switch_errors)
  return(switch_error)
}


args = commandArgs(trailingOnly=TRUE)
test_haplotypes = args[1]
truth_haplotypes = args[2]
print("Calculating switch accuracy")
print("Switch accuray is:")
print(1- get_switch_error(test_haplotypes,truth_haplotypes,random))
print("Thank you, goodbye")
