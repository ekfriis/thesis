{
  gROOT->SetStyle("Plain");

  TFile file("efficiency_data.root");

  TCanvas* canvas = (TCanvas*)file.Get(
      "/tpTree/avg_iso_pt/pt_bin0__EtaCut_pass__Glb_pass__PtThresh_pass__VBTF_pass__cbPlusExpo/fit_canvas");

  TCanvas outputCanvas("blah", "blah", 800, 600);

  TList* primitives = canvas->GetListOfPrimitives();
  for (int i = 0; i < primitives->GetSize(); i++) {
    if (i > 2)
      break;
    std::cout << "==================" << std::endl;
    TCanvas* subcanvas = (TCanvas*)primitives->At(i);
    std::cout << i << " " << subcanvas->GetName() << std::endl;
    TList* subprimitives = subcanvas->GetListOfPrimitives();
    for (int j = 0; j < subprimitives->GetSize(); j++) {
      std::cout << j << " " << subprimitives->At(j)->GetName()  <<  " " <<
        subprimitives->At(j)->IsA()->GetName() << std::endl;
    }
    RooHist* data = (RooHist*)subcanvas->GetPrimitive("h_data");
    RooCurve* pdfAll = (RooCurve*)subprimitives->At(2);
    RooCurve* pdfBkg = (RooCurve*)subprimitives->At(3);
    TH1* frame = (TH1*)subprimitives->At(0);
    frame->SetMaximum(1300);
    outputCanvas.cd();
    outputCanvas.SetLogy(false);
    frame->Draw("axis");
    data->Draw("pe");
    pdfAll->Draw();
    pdfBkg->Draw();
    TString outputName = "plot_";
    outputName += i;
    outputName += ".pdf";
    outputCanvas.Update();
    outputCanvas.SaveAs(outputName);
  }
}
