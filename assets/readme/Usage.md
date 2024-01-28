# Usage
OptiMix allows you to perform concrete mix design through a user-friendly, **five-stage process**. This section assumes familiarity with concrete materials, mix design basics , and the ``DOE method`` described in IHS BRE Press's *Design of Normal Concrete Mixes, Second Edition.*
For a detailed guidance on specific mix types (including air-entrained, pfa and ggbs mixes), please refer to to the relevant sections within the publication.

**Note:** This information forms the foundation for using OptiMix efficiently. If you're unfamiliar with these concepts, consider consulting the publication or other resources before proceeding.

All results for each stage can be viewed with the ``View Results`` button.
## Stage 1
- Specify the target compressive strength and age at test or curing,  parameters regarding variability of concrete strength during production, cement & aggregate type, restricting parameters, information concerning entrained air and ggbs proportion where applicable.
- OptiMix calculates the corresponding free water-to-cement ratio (including substitute binders where used). 

## Stage 2
- Supply the desired workability levels, coarse aggregate sizes, pfa proportion, cementing efficiency factor and water content reduction.
- OptiMix utilizes the water/binder ratio from ``Stage 1`` to determine the free-water content. 
## Stage 3
- Input the allowable cement content range and the limiting water-binder ratio (in `pfa` and `ggbs` design modes if specified.
- Combining the w/c ratio and water content from `Stage 1` & `Stage 2`, OptiMix calculates the required cement content and adjusts to specified limits accordingly.
- OptiMix proceeds with the calculated cement content if no limits are specified.
## Stage 4
- Enter the relative density of the combined aggregate in the saturated surface-dry conditions, if no detail is entered, OptiMix makes the following assumptions:
	- 2.6 for uncrushed aggregates
	- 2.7 for crushed aggregates
	- 2.65 for crushed and uncrushed aggregates.
- OptiMix makes an estimate of the density of the fully compacted concrete unless specified.
- OptiMix then determines the total aggregate content based on the cement content from `Stage 3` and the water content from `Stage 2`.
## Stage 5
- Supply the grading of fine aggregate, a percentage passing of 60% is assumed unless specified.
- In the design of air-entrained concrete mixes, OptiMix assumes a fine aggregate reduction of 5%, you can also modify this value.
- Specify the absorption of aggregates if they are to be batched in an oven-dry condition.
- OptiMix then determines fine and coarse aggregate contents.
## Final Output and Adjustments
- Upon completion, OptiMix displays the final mix proportions in kg/m<sup>3</sup>, including individual quantities for Portland cement, pfa, ggbs, fine aggregate and coarse aggregate. 
- Note that the displayed quantities for the aggregates correspond to the specified batching condition (saturated surface-dry or oven-dry).
- OptiMix uses the following ratios if 10mm, 20mm and 40mm coarse aggregates are to be combined:
	- ``1 : 2`` for a combination of 2 different aggregate sizes.
	- `1 : 1.5 : 3` for a combination of 3 different aggregate sizes.
- For trial mix preparation, easily adjust the proportions to any desired volume (m<sup>3</sup>, $\ell$) directly within the interface.
- Generate and export summaries of your mix design in multiple formats (`.docx`, `.xlsx`, `.pdf`) for documentation and future reference.


