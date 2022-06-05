// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once
#include "CoreMinimal.h"
#include "UObject/Object.h"
#include "Runtime/CoreUObject/Public/UObject/UObjectGlobals.h"


//~~~~~~~~~~~~ UMG ~~~~~~~~~~~~~~~
#include "Runtime/UMG/Public/UMG.h"
#include "Runtime/UMG/Public/UMGStyle.h"
#include "Runtime/UMG/Public/Slate/SObjectWidget.h"
#include "Runtime/UMG/Public/IUMGModule.h"
#include "Runtime/UMG/Public/Blueprint/WidgetTree.h"
#include "Runtime/UMG/Public/Blueprint/UserWidget.h"
#include "Editor/UMGEditor/Public/WidgetBlueprint.h"
#include "Runtime/SlateCore/Public/Fonts/SlateFontInfo.h"
#include "Runtime/Engine/Classes/Engine/Texture2D.h"
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#include "Kismet/BlueprintFunctionLibrary.h"
#include "FigmaImporterBPLibrary.generated.h"

/* 
*	Function library class.
*	Each function in it is expected to be static and represents blueprint node that can be called in any blueprint.
*
*	When declaring function you can define metadata for the node. Key function specifiers will be BlueprintPure and BlueprintCallable.
*	BlueprintPure - means the function does not affect the owning object in any way and thus creates a node without Exec pins.
*	BlueprintCallable - makes a function which can be executed in Blueprints - Thus it has Exec pins.
*	DisplayName - full name of the node, shown when you mouse over the node and in the blueprint drop down menu.
*				Its lets you name the node using characters not allowed in C++ function names.
*	CompactNodeTitle - the word(s) that appear on the node.
*	Keywords -	the list of keywords that helps you to find node when you search for it using Blueprint drop-down menu. 
*				Good example is "Print String" node which you can find also by using keyword "log".
*	Category -	the category your node will be under in the Blueprint drop-down menu.
*
*	For more info on custom blueprint nodes visit documentation:
*	https://wiki.unrealengine.com/Custom_Blueprint_Node_Creation
*/
UCLASS()
class UFigmaImporterBPLibrary : public UBlueprintFunctionLibrary
{
	GENERATED_UCLASS_BODY()

		UFUNCTION(BlueprintCallable)
		static void SetWidgetSizeAndPosition(UWidget* Widget, FVector2D Size, FVector2D Position, FVector2D Alignment, FVector2D MinAnchors, FVector2D MaxAnchors);
		
		UFUNCTION(BlueprintCallable)
		static void ClearContent(UWidgetBlueprint* Widget);
		
		UFUNCTION(BlueprintCallable)
		static void SetBackground(UWidgetBlueprint* Widget, FVector2D Size, FLinearColor Color);

		UFUNCTION(BlueprintCallable)
		static UUserWidget* AddChildWidget(UWidgetBlueprint* Widget, FString ChildClassPath, FName ChildWidgetName, FVector2D Size, FVector2D Position, FVector2D Alignment, FVector2D MinAnchors, FVector2D MaxAnchors);

		UFUNCTION(BlueprintCallable)
		static UImage* AddImageWidget(UWidgetBlueprint* Widget, FName Name, FVector2D Size, FVector2D Position, FString ImagePath, FVector2D Alignment, FVector2D MinAnchors, FVector2D MaxAnchors);

		UFUNCTION(BlueprintCallable)
		static UImage* AddRectangleWidget(UWidgetBlueprint* Widget, FName Name, FVector2D Size, FVector2D Position, FLinearColor Color, FVector2D Alignment, FVector2D MinAnchors, FVector2D MaxAnchors);

		UFUNCTION(BlueprintCallable)
		static UTextBlock* AddTextWidget(UWidgetBlueprint* Widget, FName Name, FString Content, FSlateFontInfo Font, FVector2D Size, FVector2D Position, FVector2D Alignment, FVector2D MinAnchors, FVector2D MaxAnchors);
};
