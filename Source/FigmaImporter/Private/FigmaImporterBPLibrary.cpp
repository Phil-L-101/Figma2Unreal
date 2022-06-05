// Copyright Epic Games, Inc. All Rights Reserved.


#include "FigmaImporterBPLibrary.h"
#include "FigmaImporter.h"

UFigmaImporterBPLibrary::UFigmaImporterBPLibrary(const FObjectInitializer& ObjectInitializer)
: Super(ObjectInitializer)
{

}

// Helper function to set slot properties of a widget
void UFigmaImporterBPLibrary::SetWidgetSizeAndPosition(UWidget* Widget, FVector2D Size, FVector2D Position, FVector2D Alignment, FVector2D MinAnchors, FVector2D MaxAnchors)
{
	if (UCanvasPanelSlot* Slot = Cast<UCanvasPanelSlot>(Widget->Slot)) {
		Slot->SetAnchors(FAnchors(MinAnchors[0], MinAnchors[1], MaxAnchors[0], MinAnchors[1]));
		Slot->SetAlignment(Alignment);
		Slot->SetSize(Size);
		Slot->SetPosition(Position);
	}

	else {
		UE_LOG(LogTemp, Warning, TEXT("Couldn't size widget"));
	}
}

// Clears all of the children from the content panel in the Frame template widget
void UFigmaImporterBPLibrary::ClearContent(UWidgetBlueprint* Widget)
{
	if(IsValid(Widget)) {
		Widget->Modify(); // Ensures asset is marked dirty for saving
		auto WidgetTree = Widget->WidgetTree;
		auto Canvas = Cast<UCanvasPanel>(WidgetTree->FindWidget("ContentPanel"));
		Canvas->ClearChildren();
	}

	else {
		UE_LOG(LogTemp, Warning, TEXT("Couldn't clear content from widget as widget not valid"));
	}
}

// Sets background colour and size of Frame template widget
void UFigmaImporterBPLibrary::SetBackground(UWidgetBlueprint* Widget, FVector2D Size, FLinearColor Color)
{
	if (IsValid(Widget)) {
		Widget->Modify(); // Ensures asset is marked dirty for saving
		auto WidgetTree = Widget->WidgetTree;
		auto Canvas = Cast<UCanvasPanel>(WidgetTree->FindWidget("BackgroundContainer"));
		auto BackgroundImage = Cast<UImage>(WidgetTree->FindWidget("BackgroundImage"));
		SetWidgetSizeAndPosition(Canvas, Size, FVector2D(0, 0), FVector2D(0.5, 0.5), FVector2D(0.5, 0.5), FVector2D(0.5, 0.5));
		BackgroundImage->SetColorAndOpacity(Color);
	}
	else{
		UE_LOG(LogTemp, Warning, TEXT("Couldn't set background for frame as widget not valid"));
	}
}

// Creates an instance of a custom UserWidget from a class path and adds it to the parent Frame template 
UUserWidget* UFigmaImporterBPLibrary::AddChildWidget(UWidgetBlueprint* Widget, FString ChildClassPath, FName ChildWidgetName, FVector2D Size, FVector2D Position, FVector2D Alignment, FVector2D MinAnchors, FVector2D MaxAnchors)
{
	if(IsValid(Widget)) {
		Widget->Modify(); // Ensures asset is marked dirty for saving

		FString BaseText = TEXT("WidgetBlueprint '");
		FString FullPath = BaseText.Append(ChildClassPath).Append(TEXT("'"));
		if (UClass* ChildBPWidgetClass = LoadClass<UUserWidget>(NULL, *FullPath))
		{
			auto WidgetTree = Widget->WidgetTree;
			UUserWidget* ChildWidget = WidgetTree->ConstructWidget<UUserWidget>(ChildBPWidgetClass, ChildWidgetName);
			auto Canvas = Cast<UCanvasPanel>(WidgetTree->FindWidget("ContentPanel"));
			Canvas->AddChild(ChildWidget);
			SetWidgetSizeAndPosition(ChildWidget, Size, Position, Alignment, MinAnchors, MaxAnchors);
			return ChildWidget;	
		}
		else {
			return NULL;
		}
	}
	else{
		UE_LOG(LogTemp, Warning, TEXT("Couldn't add child widget to frame as frame not valid"));
		return NULL;
	}
}

// Adds a basic image to a parent Frame template using a path to a Texture2D asset
UImage* UFigmaImporterBPLibrary::AddImageWidget(UWidgetBlueprint* Widget, FName Name, FVector2D Size, FVector2D Position, FString ImagePath, FVector2D Alignment, FVector2D MinAnchors, FVector2D MaxAnchors)
{
	if (IsValid(Widget)) {
		Widget->Modify(); // Ensures asset is marked dirty for saving
		auto WidgetTree = Widget->WidgetTree;
		UImage* Image = WidgetTree->ConstructWidget<UImage>(UImage::StaticClass(), Name);
		auto Canvas = Cast<UCanvasPanel>(WidgetTree->FindWidget("ContentPanel"));
		Canvas->AddChild(Image);
		UTexture2D* Texture = LoadObject<UTexture2D>(NULL, *ImagePath, NULL, LOAD_None, NULL);
		Image->SetBrushFromTexture(Texture, false);
		SetWidgetSizeAndPosition(Image, Size, Position, Alignment, MinAnchors, MaxAnchors);
		return Image;
	}
	else{
		UE_LOG(LogTemp, Warning, TEXT("Couldn't add image to frame as frame not valid"));
		return NULL;
	}
}

// Adds a basic image to parent Frame template with no texture but a colour
UImage* UFigmaImporterBPLibrary::AddRectangleWidget(UWidgetBlueprint* Widget, FName Name, FVector2D Size, FVector2D Position, FLinearColor LinearColor, FVector2D Alignment, FVector2D MinAnchors, FVector2D MaxAnchors)
{
	if (IsValid(Widget)) {
		Widget->Modify(); // Ensures asset is marked dirty for saving
		auto WidgetTree = Widget->WidgetTree;
		UImage* Image = WidgetTree->ConstructWidget<UImage>(UImage::StaticClass(), Name);
		auto Canvas = Cast<UCanvasPanel>(WidgetTree->FindWidget("ContentPanel"));
		Canvas->AddChild(Image);
		Image->SetColorAndOpacity(LinearColor);
		SetWidgetSizeAndPosition(Image, Size, Position, Alignment, MinAnchors, MaxAnchors);
		return Image;
	}
	else{
		UE_LOG(LogTemp, Warning, TEXT("Couldn't add rectangle to frame as frame not valid"));
		return NULL;
	}
}

// Adds text to a parent Frame template
UTextBlock* UFigmaImporterBPLibrary::AddTextWidget(UWidgetBlueprint* Widget, FName Name, FString Content, FSlateFontInfo Font, FVector2D Size, FVector2D Position, FVector2D Alignment, FVector2D MinAnchors, FVector2D MaxAnchors)
{
	if (IsValid(Widget)) {
		Widget->Modify(); // Ensures asset is marked dirty for saving
		auto WidgetTree = Widget->WidgetTree;
		UTextBlock* TextBlock = WidgetTree->ConstructWidget<UTextBlock>(UTextBlock::StaticClass(), Name);
		auto Canvas = Cast<UCanvasPanel>(WidgetTree->FindWidget("ContentPanel"));
		Canvas->AddChild(TextBlock);
		TextBlock->SetText(FText::AsCultureInvariant(Content));
		TextBlock->SetFont(Font);
		SetWidgetSizeAndPosition(TextBlock, Size, Position, Alignment, MinAnchors, MaxAnchors);
		return TextBlock;
	}
	else{
		UE_LOG(LogTemp, Warning, TEXT("Couldn't text to frame as frame not valid"));
		return NULL;
	}
}

