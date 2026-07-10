namespace DoomMapGuessr.Enums;


    /// <summary>
    /// Supported image aspect ratios.
    /// </summary>
    public enum AspectRatio
    {

        /// <summary>
        /// Original image proportions.
        /// </summary>
        Maintain,

        /// <summary>
        /// Landspace 16:9 image aspect ratio.
        /// </summary>
        Landscape16_9,

        /// <summary>
        /// Landspace 16:9 image aspect ratio.
        /// Often associated with retro imagery.
        /// </summary>
        Landscape4_3,

        /// <summary>
        /// Square 1:1 image aspect ratio.
        /// All n:n aspect ratios fit in this category.
        /// </summary>
        Square1_1

    }
